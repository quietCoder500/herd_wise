from django.urls import path
from apps.livestock import views

urlpatterns = [
    path("farm/", views.farm_list),
    path("farm/<str:short_uuid>/", views.farm_detail),
]
