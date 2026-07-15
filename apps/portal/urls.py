from django.urls import path

from apps.portal import views

app_name = "portal"

urlpatterns = [
    path("", views.index, name="index_view"),
    path("search", views.Search.as_view(), name="search_view"),
    path("records", views.all_records_list_view, name="all_records_list_view"),
    path(
        "records/<uuid:public_id>",
        views.RecordsDetailView.as_view(),
        name="records_detail_view",
    ),
    path("farms", views.farms_list_view, name="farms_list_view"),
    path("farms/create", views.farms_create_view, name="farms_create_view"),
    path("farms/<str:slug>", views.farms_detail_view, name="farms_detail_view"),
    path("farms/<str:slug>/herds", views.herds_list_view, name="herds_list_view"),
    path(
        "farms/<str:slug>/herds/create",
        views.herds_create_view,
        name="herds_create_view",
    ),
    path("herds/<str:slug>", views.herds_detail_view, name="herds_detail_view"),
    path(
        "herds/<str:slug>/animals",
        views.animals_list_view,
        name="animals_list_view",
    ),
    path(
        "herds/<str:slug>/animals/create",
        views.animals_create_view,
        name="animals_create_view",
    ),
    path(
        "herds/<str:slug>/animals/mass_create",
        views.mass_create_animals_view,
        name="animals_mass_create_view",
    ),
    path(
        "animals/<str:slug>",
        views.animals_detail_view,
        name="animals_detail_view",
    ),
    path("tags/read", views.tags_read_view, name="tags_read_view"),
    path("tags/write/<str:slug>", views.tags_write_view, name="tags_write_view"),
    path(
        "herds/<slug:slug>/records",
        views.RecordsListView.as_view(),
        name="records_list_view",
    ),
    path(
        "herds/<slug:slug>/records/<slug:form_slug>",
        views.RecordsCreateView.as_view(),
        name="herd_records_create_view",
    ),
    path(
        "animals/<slug:slug>/records",
        views.RecordsListView.as_view(),
        name="records_list_view",
    ),
    path(
        "animals/<slug:slug>/records/<slug:form_slug>",
        views.RecordsCreateView.as_view(),
        name="animal_records_create_view",
    ),
]
