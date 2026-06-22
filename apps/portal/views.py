from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from itertools import chain

from apps.portal.forms import DynamicRecordForm
from apps.portal.models import (
    Animal,
    AnimalGroup,
    Farm,
    RecordTemplate,
    LivestockRecord,
    ReportableModel,
)
from utils.lib import AlpineTemplateResponse


@login_required
def index(request):
    return render(request, "portal/index.html")


class Search(LoginRequiredMixin, View):
    def get(self, request):
        query = request.GET.get("search", "").strip()

        farms = Farm.objects.none()
        animal_groups = AnimalGroup.objects.none()
        animals = Animal.objects.none()

        if query:
            farms = Farm.objects.filter(name__icontains=query)
            animal_groups = AnimalGroup.objects.filter(name__icontains=query)

            animals = Animal.objects.filter(
                Q(name__icontains=query)
                | Q(tag_id__icontains=query)
                | Q(breed__icontains=query)
                | Q(group_index__icontains=query)
            )

        context = {
            "results": list(chain(farms, animal_groups, animals)),
            "filters": {"farms": None, "herds": None, "record_types": None},
        }

        return AlpineTemplateResponse(request, "portal/search.html", context=context)


class AddRecordTemplateView(LoginRequiredMixin, View):
    def get(self, request):
        # TODO: Handle CSRF token
        return render(request, "portal/add_record_template.html")

    def post(self, request):

        return render(request, "portal/add_record_template.html")


class AddRecordView(LoginRequiredMixin, View):
    def get(self, request, template_slug):
        template = get_object_or_404(RecordTemplate, slug=template_slug)
        model_options = ReportableModel.objects.filter(farm__users=request.user)
        form = DynamicRecordForm(template=template, model_options=model_options)

        return render(
            request, "portal/add_record.html", {"form": form, "template": template}
        )

    def post(self, request, template_slug):
        template = get_object_or_404(RecordTemplate, slug=template_slug)
        model_options = ReportableModel.objects.filter(farm__users=request.user)
        form = DynamicRecordForm(
            request.POST, template=template, model_options=model_options
        )
        if form.is_valid():
            LivestockRecord.objects.create(
                report_link=form.cleaned_data.pop("report_link"),
                template=template,
                data=form.cleaned_data,
            ).save()

        return render(
            request, "portal/add_record.html", {"form": form, "template": template}
        )
