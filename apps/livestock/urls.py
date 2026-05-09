from django.urls import path

from apps.livestock import views

app_name = "livestock"

urlpatterns = [
    path("", views.index),
    path("farm/<str:farm_pub_id>", views.animal_group_col)
]
