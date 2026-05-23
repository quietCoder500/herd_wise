from django.urls import path

from apps.livestock import views

app_name = "livestock"

urlpatterns = [
    path("", views.index, name="index"),
]
