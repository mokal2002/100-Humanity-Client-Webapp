from django.urls import path
from apps.videos import views

app_name = "videos"

urlpatterns = [
    path("", views.video_list_view, name="video_list"),
    path("<slug:slug>/", views.video_detail_view, name="video_detail"),
]
