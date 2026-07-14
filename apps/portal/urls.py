from django.urls import path

from apps.portal import views

app_name = "portal"

urlpatterns = [
    path("", views.index, name="index_view"),
    path("search", views.Search.as_view(), name="search_view"),
    path("records", views.records_list_view, name="records_list_view"),
    path("farms", views.farms_list_view, name="farms_list_view"),
    path("farms/create", views.farms_create_view, name="farms_create_view"),
    path("farms/<str:farm_pub_id>", views.farms_detail_view, name="farms_detail_view"),
    path(
        "farms/<str:farm_pub_id>/herds", views.herds_list_view, name="herds_list_view"
    ),
    path(
        "farms/<str:farm_pub_id>/herds/create",
        views.herds_create_view,
        name="herds_create_view",
    ),
    path("herds/<str:herd_pub_id>", views.herds_detail_view, name="herds_detail_view"),
    path(
        "herds/<str:herd_pub_id>/animals",
        views.animals_list_view,
        name="animals_list_view",
    ),
    path(
        "herds/<str:herd_pub_id>/animals/create",
        views.animals_create_view,
        name="animals_create_view",
    ),
    path(
        "animals/<str:animal_pub_id>",
        views.animals_detail_view,
        name="animals_detail_view",
    ),
    path("tags/read", views.tags_read_view, name="tags_read_view"),
    path(
        "tags/write/<str:animal_pub_id>", views.tags_write_view, name="tags_write_view"
    ),
]
