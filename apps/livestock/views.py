from django.shortcuts import render
from apps.livestock.models import Farm, AnimalGroup, Animal


def dashboard_home(request):
    farm_objs = Farm.objects.get()
    miller_columns = [
        {"id": 1, "header": "", "models": farm_objs},
    ]
    return render(
        request, "livestock/dashboard/index.html", context={"columns": miller_columns}
    )
