from django.contrib.auth.decorators import login_required
from django.views import View
from django.shortcuts import get_list_or_404, get_object_or_404, render
from django.urls import reverse_lazy as reverse

from apps.portal.models import Animal, AnimalGroup, Farm
from utils.lib import AlpineTemplateResponse

def index(request):
    return render(request, "portal/index.html")

class Search(View):
    def get(self, request):
        return AlpineTemplateResponse(request, "portal/search.html")
