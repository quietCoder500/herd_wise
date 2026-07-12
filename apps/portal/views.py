from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from django.views import View
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.db.models import Q
from django.utils.text import slugify

from apps.portal.forms import DynamicRecordForm, SchemaFieldFormSet, FarmForm
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
        normalized_query = " ".join(query.split()).lower()

        if not normalized_query:
            results = []
        else:
            user_farms = Farm.objects.filter(users=request.user)
            farms = user_farms.filter(name__icontains=query)
            animal_groups = AnimalGroup.objects.filter(
                farm__in=user_farms, name__icontains=query
            )
            animals = Animal.objects.filter(
                Q(name__icontains=query)
                | Q(breed__icontains=query)
                | Q(tag_id__icontains=query)
                | Q(group_index__icontains=query),
                farm__in=user_farms,
            )

            def score_result(label: str) -> int:
                lowered_label = label.lower()
                if lowered_label == normalized_query:
                    return 100
                if lowered_label.startswith(normalized_query):
                    return 80
                if normalized_query in lowered_label:
                    return 60
                return 0

            results = []
            for farm in farms:
                results.append(
                    {
                        "label": farm.name,
                        "kind": "Farm",
                        "score": score_result(farm.name),
                        "url": reverse(
                            "portal:farms_detail_view",
                            kwargs={"public_id": farm.public_id},
                        ),
                    }
                )
            for herd in animal_groups:
                results.append(
                    {
                        "label": herd.name,
                        "kind": "Herd",
                        "score": score_result(herd.name),
                        "url": reverse(
                            "portal:herds_detail_view",
                            kwargs={"public_id": herd.public_id},
                        ),
                    }
                )
            for animal in animals:
                results.append(
                    {
                        "label": animal.formatted_name,
                        "kind": "Animal",
                        "score": score_result(animal.formatted_name),
                        "url": reverse(
                            "portal:animals_detail_view",
                            kwargs={"public_id": animal.public_id},
                        ),
                    }
                )

            results.sort(key=lambda item: item["score"], reverse=True)

        context = {
            "results": results,
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


@login_required
def farms_list_view(request):
    farms = get_list_or_404(Farm, users=request.user)
    return render(request, "portal/farms/farms_list.html", {"farms": farms})


@login_required
def farms_detail_view(request, public_id):
    farm = get_object_or_404(Farm, public_id=public_id)
    form = FarmForm(instance=farm)
    return render(request, "portal/farms/farms_view.html", {"form": form})


@login_required
def herds_detail_view(request, public_id):
    herd = get_object_or_404(AnimalGroup, public_id=public_id)
    return render(request, "portal/herds/herds_view.html", {"herd": herd})


@login_required
def animals_detail_view(request, public_id):
    animal = get_object_or_404(Animal, public_id=public_id)
    return render(request, "portal/animals/animals_view.html", {"animal": animal})


@login_required
def farms_create_view(request):
    if request.method == "POST":
        form = FarmForm(request.POST)
        if form.is_valid():
            new_farm = form.save()
            new_farm.users.add(request.user)
            new_farm.save()

            print(new_farm.public_id)
            return redirect(
                reverse(
                    "portal:farms_detail_view", kwargs={"public_id": new_farm.public_id}
                )
            )
        else:
            return render(
                request, "portal/farms/farms_create.html", context={"form": form}
            )
    else:
        form = FarmForm()
        return render(request, "portal/farms/farms_create.html", context={"form": form})
