from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.livestock.models import Farm, AnimalGroup, Animal
from utils.lib import AlpineTemplateResponse

# TODO: Convert all filters to objects or 404

@login_required
def index(request):
    """Renders the column containing all farms related to the user"""
    farm_objs = Farm.objects.filter(users=request.user)
    return AlpineTemplateResponse(
        request, "livestock/dashboard/index.html", context={"farms": farm_objs}
    )

@login_required
def farm_col(request, farm_pub_id):
    """Renders the column containing all animal groups related to this farm"""
    context = {"groups": AnimalGroup.objects.filter(farm__public_id=farm_pub_id, farm__users=request.user)}
    return AlpineTemplateResponse(request, "livestock/dashboard/index.html", context)

@login_required
def group_col(request, group_pub_id):
    context = {"animals": Animal.objects.filter(group__public_id=group_pub_id, group__farm__users=request.user)}
    return AlpineTemplateResponse(request, "livestock/dashboard/index.html", context)

@login_required
def animal_col(request, animal_pub_id):
    context = {"animals": Animal.objects.filter(public_id=animal_pub_id)}
    return AlpineTemplateResponse(request, "livestock/dashboard/index.html", context)


