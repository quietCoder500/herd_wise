from django.urls import path

from apps.portal import views

app_name = "portal"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.Search.as_view(), name="search"),
]
