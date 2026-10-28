from django.urls import path
from apps.education import views

app_name = "education"

urlpatterns = [
    path("", views.principle_list_view, name="principle_list"),
]
