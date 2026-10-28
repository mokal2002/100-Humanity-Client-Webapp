from django.urls import path
from apps.gallery import views

app_name = "gallery"

urlpatterns = [
    path("", views.album_list_view, name="album_list"),
    path("upload/", views.bulk_upload_view, name="bulk_upload"),
    path("photo/<int:pk>/delete/", views.delete_image_view, name="delete_image"),
    path("album/<slug:slug>/", views.album_detail_view, name="album_detail"),
]
