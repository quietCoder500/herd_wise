from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render

from apps.livestock.models import Animal, AnimalGroup, Farm


class Breadcrumbs:
    HOME = {"title": "Home", "icon": None, "view": "livestock_index"}
    FARMS = {"title": "Farms", "icon": None, "view": "farm_list"}


#
# Non-model specific views
#


def index(request):
    breadcrumbs = [Breadcrumbs.HOME]
    return render(request, "livestock/index.html", context={"breadcrumbs": breadcrumbs})


#
# Views for models
#


@login_required
def farm_list(request):
    breadcrumbs = [Breadcrumbs.HOME, Breadcrumbs.FARMS]
    # 404 will need to be later removed to show a proper page or redirect if there are no farms
    farms = get_list_or_404(Farm, users=request.user)

    return render(
        request,
        "livestock/farm/list.html",
        context={"breadcrumbs": breadcrumbs, "farms": farms},
    )


@login_required
def farm_detail(request, short_uuid):
    breadcrumbs = [Breadcrumbs.HOME, Breadcrumbs.FARMS]
    obj = get_object_or_404(Farm, public_id=short_uuid)
    breadcrumbs.append({"title": obj.name, "icon": None, "url": None})
    return render(
        request,
        "livestock/farm/detailed.html",
        context={"breadcrumbs": breadcrumbs, "farm": obj},
    )


@login_required
def animal_group_list(request, farm_short_uuid):
    animal_groups = get_list_or_404(
        AnimalGroup, farm__users=request.user, farm__public_id=farm_short_uuid
    )
    return render(
        request,
        "livestock/animal_group/list.html",
        context={"animal_groups": animal_groups},
    )


@login_required
def animal_group_detail(request, short_uuid):
    obj = get_object_or_404(AnimalGroup, public_id=short_uuid)
    return render(
        request, "livestock/animal_group/detailed.html", context={"animal_group": obj}
    )


@login_required
def animal_list(request, animal_group_short_uuid):
    animals = get_list_or_404(Animal, group__public_id=animal_group_short_uuid)
    return render(request, "livestock/animal/list.html", context={"animals": animals})


@login_required
def animal_detail(request, short_uuid):
    obj = get_object_or_404(Animal, public_id=short_uuid)
    return render(request, "livestock/animal/detailed.html", context={"animal": obj})
