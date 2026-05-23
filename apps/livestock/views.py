from django.contrib.auth.decorators import login_required
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse_lazy as reverse

from apps.livestock.models import Animal, AnimalGroup, Farm

def index(request):
    return render(request, "dashboard/index.html")
