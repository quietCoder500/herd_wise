from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, get_list_or_404, render
from apps.livestock.models import Farm


@login_required
def farm_list(request):
    # 404 will need to be later removed to show a proper page or redirect if there are no farms
    farms = get_list_or_404(Farm, users=request.user)
    html = ""
    for farm in farms:
        html += f"{farm.name}, "
    return render(request, "livestock/farm/list.html", context={"farms": farms})

@login_required
def farm_detail(request, short_uuid):
    obj = get_object_or_404(Farm, public_id=short_uuid)
    return render(request, "livestock/farm/detailed.html", context={"farm": obj})

def animal_group_list():
    pass

def animal_group_detail():
    pass

def animal_list():
    pass

def animal_detail():
    pass
