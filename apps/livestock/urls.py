from django.urls import path
from apps.livestock import views

urlpatterns = [
    path("farms/", views.farm_list),
    path("farm/<str:short_uuid>/", views.farm_detail),
    path("animal_groups/<str:farm_short_uuid>/", views.animal_group_list),
    path("animal_group/<str:short_uuid>/", views.animal_group_detail),
    path("animals/<str:animal_group_short_uuid>/", views.animal_list),
    path("animal/<str:short_uuid>/", views.animal_detail),
]
