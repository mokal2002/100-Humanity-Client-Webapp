"""
Public and staff-protected views for Photo Gallery albums, responsive grids,
multi-image bulk upload with preview, and confirmed image deletion.
"""
import os
from django.contrib import messages
from django.contrib.admin.views.decorators import staff_member_required
from django.core.paginator import Paginator
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from apps.gallery.forms import BulkGalleryUploadForm
from apps.gallery.models import GalleryAlbum, GalleryImage
from apps.gallery.services import upload_image_to_cloudinary


def album_list_view(request):
    """Lists published photo albums, categories, and recent photographs with pagination."""
    selected_category = request.GET.get("category", "").strip()

    albums_qs = GalleryAlbum.objects.filter(is_published=True).annotate(
        published_photos_count=Count("images", filter=Q(images__is_published=True))
    )
    if selected_category:
        albums_qs = albums_qs.filter(category__iexact=selected_category)

    categories = (
        GalleryAlbum.objects.filter(is_published=True)
        .values_list("category", flat=True)
        .distinct()
        .order_by("category")
    )

    photos_qs = (
        GalleryImage.objects.filter(is_published=True, album__is_published=True)
        .select_related("album")
        .order_by("display_order", "-created_at")
    )
    if selected_category:
        photos_qs = photos_qs.filter(album__category__iexact=selected_category)

    paginator = Paginator(photos_qs, 12)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "gallery/album_list.html",
        {
            "albums": albums_qs,
            "categories": categories,
            "selected_category": selected_category,
            "page_obj": page_obj,
        },
    )


def album_detail_view(request, slug):
    """Displays all published photographs inside a specific album with full-screen lightbox support."""
    album = get_object_or_404(GalleryAlbum, slug=slug, is_published=True)
    photos_qs = album.images.filter(is_published=True).order_by("display_order", "-created_at")
    paginator = Paginator(photos_qs, 16)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "gallery/album_detail.html",
        {
            "album": album,
            "page_obj": page_obj,
        },
    )


@staff_member_required
def bulk_upload_view(request):
    """
    Allows authorized staff/administrators to upload multiple photographs in one workflow
    with client-side image previews before submission and server-side Cloudinary upload.
    """
    if request.method == "POST":
        form = BulkGalleryUploadForm(request.POST, request.FILES)
        if form.is_valid():
            album = form.cleaned_data["album"]
            prefix = form.cleaned_data.get("default_caption_prefix", "").strip()
            files = form.cleaned_data["images"]

            success_count = 0
            errors = []
            for idx, f in enumerate(files, start=1):
                res = upload_image_to_cloudinary(f, subfolder=f"gallery/{album.slug}")
                if res.success:
                    raw_name = os.path.splitext(f.name)[0].replace("-", " ").replace("_", " ").strip()
                    title = f"{prefix} — {idx}" if prefix else (raw_name.title() or f"{album.title} Photo {idx}")
                    GalleryImage.objects.create(
                        album=album,
                        title=title[:200],
                        alt_text=title[:220],
                        image_url=res.secure_url,
                        cloudinary_public_id=res.public_id,
                        width=res.width,
                        height=res.height,
                        display_order=idx,
                        is_published=True,
                    )
                    success_count += 1
                else:
                    errors.append(f"{f.name}: {res.error_message}")

            if success_count:
                messages.success(
                    request,
                    f"Successfully uploaded {success_count} photograph(s) to '{album.title}'.",
                )
            for err in errors:
                messages.error(request, err)

            if success_count and not errors:
                return redirect(album.get_absolute_url())
    else:
        initial_album = request.GET.get("album")
        form = BulkGalleryUploadForm(initial={"album": initial_album} if initial_album else None)

    return render(request, "gallery/bulk_upload.html", {"form": form})


@staff_member_required
@require_POST
def delete_image_view(request, pk):
    """Staff-only endpoint to delete a gallery photograph (with confirmation in UI and Cloudinary cleanup)."""
    image = get_object_or_404(GalleryImage, pk=pk)
    album_url = image.album.get_absolute_url()
    title = image.title
    image.delete()
    messages.success(request, f"Photograph '{title}' has been deleted.")
    return redirect(album_url)
