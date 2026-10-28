from django.urls import path
from apps.articles import views

app_name = "articles"

urlpatterns = [
    path("", views.article_list_view, name="article_list"),
    path("<slug:slug>/", views.article_detail_view, name="article_detail"),
]
