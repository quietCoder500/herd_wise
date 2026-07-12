from django.urls import path

from apps.portal import views

app_name = "portal"

urlpatterns = [
    path("", views.index, name="index_view"),
    path("search", views.Search.as_view(), name="search_view"),
    path("farms", views.farms_list_view, name="farms_list_view"),
    path("farms/create", views.farms_create_view, name="farms_create_view"),
    path("farms/<str:public_id>", views.farms_detail_view, name="farms_detail_view"),
    path("herds/<str:public_id>", views.herds_detail_view, name="herds_detail_view"),
    path(
        "animals/<str:public_id>", views.animals_detail_view, name="animals_detail_view"
    ),
]
