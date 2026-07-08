from django.urls import path

from apps.portal import views

app_name = "portal"

urlpatterns = [
    path("", views.index, name="index"),
    path("search", views.Search.as_view(), name="search"),
    path(
        "record-template",
        views.AddRecordTemplateView.as_view(),
        name="add_record_template",
    ),
    path(
        "livestock-record/create/<slug:template_slug>/",
        views.AddRecordView.as_view(),
        name="add_livestock_record",
    ),
    path(
        "livestock-record/view/<uuid:public_id>/",
        views.GetRecordView.as_view(),
        name="get_record_view",
    ),
]
