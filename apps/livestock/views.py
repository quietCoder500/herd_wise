from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse_lazy as reverse

from apps.livestock.models import Animal, AnimalGroup, Farm


class Breadcrumbs:
    """Factory for building breadcrumb trails.

    Each factory method returns a list of breadcrumb dicts where each dict
    contains at least: title, view, and url. Callers can copy or extend the
    returned list.
    """

    @staticmethod
    def home():
        return {
            "title": "Home",
            "icon": None,
            "view": "livestock_index",
            "url": reverse("livestock:index"),
        }

    @staticmethod
    def farms():
        return {
            "title": "Farms",
            "icon": None,
            "view": "farm_list",
            "url": reverse("livestock:farm_list"),
        }

    @staticmethod
    def farm(farm_obj):
        # Accept either a Farm instance or its public_id
        public_id = getattr(farm_obj, "public_id", farm_obj)
        name = getattr(farm_obj, "name", str(public_id))
        return {
            "title": name,
            "icon": None,
            "view": "farm_detail",
            "args": [public_id],
            "url": reverse("livestock:farm_detail", args=[public_id]),
        }

    @staticmethod
    def animal_group_list(farm_obj):
        public_id = getattr(farm_obj, "public_id", farm_obj)
        return {
            "title": "Animal groups",
            "icon": None,
            "view": "animal_group_list",
            "args": [public_id],
            "url": reverse("livestock:animal_group_list", args=[public_id]),
        }

    @staticmethod
    def animal_group(obj):
        public_id = getattr(obj, "public_id", obj)
        name = getattr(obj, "name", str(public_id))
        return {
            "title": name,
            "icon": None,
            "view": "animal_group_detail",
            "args": [public_id],
            "url": reverse("livestock:animal_group_detail", args=[public_id]),
        }

    @staticmethod
    def animal_list(group_obj):
        public_id = getattr(group_obj, "public_id", group_obj)
        return {
            "title": "Animals",
            "icon": None,
            "view": "animal_list",
            "args": [public_id],
            "url": reverse("livestock:animal_list", args=[public_id]),
        }

    @staticmethod
    def animal(obj):
        public_id = getattr(obj, "public_id", obj)
        name = getattr(obj, "name", str(public_id))
        return {
            "title": name,
            "icon": None,
            "view": "animal_detail",
            "args": [public_id],
            "url": reverse("livestock:animal_detail", args=[public_id]),
        }


#
# Non-model specific views
#


def index(request):
    breadcrumbs = [Breadcrumbs.home()]
    return render(request, "livestock/index.html", context={"breadcrumbs": breadcrumbs})


#
# Views for models
#


@login_required
def farm_list(request):
    breadcrumbs = [Breadcrumbs.home(), Breadcrumbs.farms()]
    farms = get_list_or_404(Farm, users=request.user)

    return render(
        request,
        "livestock/farm/list.html",
        context={"breadcrumbs": breadcrumbs, "farms": farms},
    )


@login_required
def farm_detail(request, short_uuid):
    obj = get_object_or_404(Farm, public_id=short_uuid)
    breadcrumbs = [Breadcrumbs.home(), Breadcrumbs.farms(), Breadcrumbs.farm(obj)]
    return render(
        request,
        "livestock/farm/detailed.html",
        context={"breadcrumbs": breadcrumbs, "farm": obj},
    )


@login_required
def animal_group_list(request, farm_short_uuid):
    farm = get_object_or_404(Farm, public_id=farm_short_uuid, users=request.user)
    breadcrumbs = [
        Breadcrumbs.home(),
        Breadcrumbs.farms(),
        Breadcrumbs.farm(farm),
        Breadcrumbs.animal_group_list(farm),
    ]

    animal_groups = get_list_or_404(
        AnimalGroup, farm__users=request.user, farm__public_id=farm_short_uuid
    )
    return render(
        request,
        "livestock/animal_group/list.html",
        context={
            "breadcrumbs": breadcrumbs,
            "animal_groups": animal_groups,
            "farm": farm,
        },
    )


@login_required
def animal_group_detail(request, short_uuid):
    obj = get_object_or_404(AnimalGroup, public_id=short_uuid)
    farm = obj.farm
    breadcrumbs = [
        Breadcrumbs.home(),
        Breadcrumbs.farms(),
        Breadcrumbs.farm(farm),
        Breadcrumbs.animal_group_list(farm),
        Breadcrumbs.animal_group(obj),
    ]
    return render(
        request,
        "livestock/animal_group/detailed.html",
        context={"animal_group": obj, "breadcrumbs": breadcrumbs},
    )


@login_required
def animal_list(request, animal_group_short_uuid):
    group = get_object_or_404(AnimalGroup, public_id=animal_group_short_uuid)
    farm = group.farm
    breadcrumbs = [
        Breadcrumbs.home(),
        Breadcrumbs.farms(),
        Breadcrumbs.farm(farm),
        Breadcrumbs.animal_group_list(farm),
        Breadcrumbs.animal_group(group),
        Breadcrumbs.animal_list(group),
    ]
    animals = get_list_or_404(Animal, group__public_id=animal_group_short_uuid)
    return render(
        request,
        "livestock/animal/list.html",
        context={"animals": animals, "breadcrumbs": breadcrumbs, "group": group},
    )


@login_required
def animal_detail(request, short_uuid):
    obj = get_object_or_404(Animal, public_id=short_uuid)
    group = obj.group
    farm = group.farm
    breadcrumbs = [
        Breadcrumbs.home(),
        Breadcrumbs.farms(),
        Breadcrumbs.farm(farm),
        Breadcrumbs.animal_group_list(farm),
        Breadcrumbs.animal_group(group),
        Breadcrumbs.animal_list(group),
        Breadcrumbs.animal(obj),
    ]
    return render(
        request,
        "livestock/animal/detailed.html",
        context={"animal": obj, "breadcrumbs": breadcrumbs},
    )
