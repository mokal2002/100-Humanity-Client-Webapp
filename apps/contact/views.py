"""
Views for the Contact Us page with basic session rate-limiting and database persistence.
"""
import time
from django.contrib import messages
from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.translation import gettext as _
from apps.contact.forms import ContactForm


def contact_view(request):
    is_ajax = (
        request.headers.get("x-requested-with") == "XMLHttpRequest"
        or request.content_type == "application/json"
        or "application/json" in request.headers.get("accept", "")
    )

    if request.method == "POST":
        # Basic session cooldown check (prevent rapid automated flooding)
        last_submit_ts = request.session.get("last_contact_submit_ts", 0)
        now_ts = time.time()
        if now_ts - last_submit_ts < 5:
            msg = _("Please wait a few seconds before submitting another message.")
            if is_ajax:
                return JsonResponse({"status": "error", "message": msg}, status=429)
            messages.error(request, msg)
            return redirect("contact:contact")

        form = ContactForm(request.POST)
        if form.is_valid():
            form.save()
            request.session["last_contact_submit_ts"] = now_ts
            msg = _(
                "Thank you for reaching out to 100% HUMANITY! Your message has been securely "
                "recorded and Arvind Betkar will review it soon."
            )
            if is_ajax:
                return JsonResponse({"status": "ok", "message": msg})
            messages.success(request, msg)
            return redirect("contact:contact")
        else:
            msg = _("Please correct the highlighted errors in the form below.")
            if is_ajax:
                errors = {}
                for field, err_list in form.errors.items():
                    errors[field] = [str(e) for e in err_list]
                return JsonResponse({"status": "error", "message": msg, "errors": errors}, status=400)
            messages.error(request, msg)
    else:
        form = ContactForm()

    return render(request, "contact/contact.html", {"form": form})
