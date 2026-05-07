from django.urls import path

from apps.livestock import views

app_name = "livestock"

urlpatterns = [
    path("", views.index, name="index"),
    path("farms/", views.farm_list, name="farm_list"),
    path("farm/<str:short_uuid>/", views.farm_detail, name="farm_detail"),
    path(
        "animal_groups/<str:farm_short_uuid>/",
        views.animal_group_list,
        name="animal_group_list",
    ),
    path(
        "animal_group/<str:short_uuid>/",
        views.animal_group_detail,
        name="animal_group_detail",
    ),
    path(
        "animals/<str:animal_group_short_uuid>/", views.animal_list, name="animal_list"
    ),
    path("animal/<str:short_uuid>/", views.animal_detail, name="animal_detail"),
]
