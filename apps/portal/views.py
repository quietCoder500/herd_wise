from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import View
from django.shortcuts import get_object_or_404, render
from django.db.models import Q
from django.utils.text import slugify
from itertools import chain

from apps.portal.forms import DynamicRecordForm, SchemaFieldFormSet
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
        formset = SchemaFieldFormSet()
        return render(request, "portal/add_record_template.html", {"formset": formset})

    def post(self, request):
        formset = SchemaFieldFormSet(request.POST)
        if formset.is_valid():
            schema_data = []

            for form in formset.ordered_forms:
                schema_data.append(
                    {
                        "name": slugify(form.cleaned_data.get("label")),  # type: ignore
                        "label": form.cleaned_data.get("label"),
                        "field_type": form.cleaned_data.get("field_type", "text"),
                        "required": form.cleaned_data.get("required", True),
                    }
                )
            # For tomorrow me: Add another form using ModelForm for the RecordTemplate model's extra data
            # then create a validation for the schema, then save the model to the DB. Also, copy django's default form templates and add daisy UI to them.

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


class _RecordField:
    def __init__(
        self, name: str, label: str, data_type: str, required: bool, value
    ) -> None:
        self.name = name
        self.label = label
        self.data_type = data_type
        self.required = required
        self.value = value


class GetRecordView(LoginRequiredMixin, View):
    def get(self, request, public_id):
        record = get_object_or_404(
            LivestockRecord, report_link__farm__users=request.user, public_id=public_id
        )
        fields = []
        schema = record.template.schema
        for field in schema:
            print(field)
            fields.append(
                _RecordField(
                    name=field.get("name"),
                    label=field.get("label"),
                    data_type=field.get("field_type"),
                    required=field.get("required"),
                    value=record.data.get(field.get("name")),
                )
            )
        context = {"fields": fields, "template_name": record.template.name}
        return render(request, "portal/models/record_read.html", context=context)
