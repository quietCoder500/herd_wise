from django.urls import path

from apps.livestock import views

app_name = "livestock"

urlpatterns = [
    path("", views.index, name="farms-col"),
    path("farm/<str:farm_pub_id>", views.farm_col, name="farm"),
    path("group/<str:group_pub_id>", views.group_col, name="group"),
    path("animal/<str:animal_pub_id>", views.animal_col, name="animal")
]
