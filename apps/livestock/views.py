from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.livestock.models import Farm, AnimalGroup, Animal
from utils.lib import AlpineTemplateResponse

@login_required
def index(request):
    farm_objs = Farm.objects.filter(users=request.user)
    return AlpineTemplateResponse(
        request, "livestock/dashboard/index.html", context={"farms": farm_objs}
    )

@login_required
def animal_group_col(request, farm_pub_id):
    context = {"groups": AnimalGroup.objects.filter(farm__public_id=farm_pub_id, farm__users=request.user)}
    return AlpineTemplateResponse(request, "livestock/dashboard/index.html", context)