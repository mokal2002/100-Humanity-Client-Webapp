from django.urls import path
from apps.events import views

app_name = "events"

urlpatterns = [
    path("", views.event_list_view, name="event_list"),
    path("<slug:slug>/", views.event_detail_view, name="event_detail"),
]
