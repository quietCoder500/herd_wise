from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.http import HttpResponseNotFound
from django.urls import reverse
from django.views import View
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.db.models import Q
from django.utils.text import slugify

from apps.portal.forms import (
    DynamicRecordForm,
    HerdForm,
    MassAnimalForm,
    SchemaFieldFormSet,
    FarmForm,
    AnimalForm,
)
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


@login_required
def records_list_view(request):
    return HttpResponseNotFound("No page here yet")


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
                            kwargs={"farm_pub_id": farm.public_id},
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
                            kwargs={"herd_pub_id": herd.public_id},
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
                            kwargs={"animal_pub_id": animal.public_id},
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


#
# Farms
#


@login_required
def farms_list_view(request):
    farms = get_list_or_404(Farm, users=request.user)
    return render(request, "portal/farms/farms_list.html", {"farms": farms})


@login_required
def farms_detail_view(request, farm_pub_id):
    farm = get_object_or_404(Farm, public_id=farm_pub_id)
    form = FarmForm(instance=farm)
    return render(request, "portal/farms/farms_view.html", {"form": form})


@login_required
def farms_create_view(request):
    if request.method == "POST":
        form = FarmForm(request.POST)
        if form.is_valid():
            with transaction.atomic():
                new_farm = form.save()
                new_farm.users.add(request.user)
                new_farm.save()
            messages.success(request, f"Successfully created farm {new_farm.name}.")
            return redirect(
                reverse(
                    "portal:farms_detail_view",
                    kwargs={"farm_pub_id": new_farm.public_id},
                )
            )
        else:
            return render(
                request, "portal/farms/farms_create.html", context={"form": form}
            )
    else:
        form = FarmForm()
        return render(request, "portal/farms/farms_create.html", context={"form": form})


#
# Herds
#


@login_required
def herds_list_view(request, farm_pub_id):
    farm = get_object_or_404(Farm, users=request.user, public_id=farm_pub_id)
    herds = get_list_or_404(AnimalGroup, farm=farm)
    return render(
        request,
        "portal/herds/herds_list.html",
        {"herds": herds, "farm_pub_id": farm_pub_id},
    )


@login_required
def herds_create_view(request, farm_pub_id):
    farm = get_object_or_404(Farm, users=request.user, public_id=farm_pub_id)
    if request.method == "POST":
        form = HerdForm(request.POST)
        if form.is_valid():
            new_herd = form.save(commit=False)
            new_herd.farm = farm
            new_herd.save()
            messages.success(request, f"Successfully created herd {new_herd.name}.")
            return redirect(
                reverse(
                    "portal:herds_detail_view",
                    kwargs={"herd_pub_id": new_herd.public_id},
                )
            )
        else:
            return render(
                request,
                "portal/herds/herds_create.html",
                {"form": form, "farm_pub_id": farm_pub_id},
            )
    return render(
        request,
        "portal/herds/herds_create.html",
        {"form": HerdForm(), "farm_pub_id": farm_pub_id},
    )


@login_required
def herds_detail_view(request, herd_pub_id):
    herd = get_object_or_404(AnimalGroup, public_id=herd_pub_id)
    form = HerdForm(instance=herd)
    if request.method == "POST":
        form = HerdForm(request.POST, instance=herd)
        if form.is_valid():
            form.save()
            messages.success(request, f"Successfully updated herd {herd.name}.")
            return redirect(
                reverse(
                    "portal:herds_detail_view",
                    kwargs={"herd_pub_id": herd.public_id},
                )
            )
        else:
            return render(
                request,
                "portal/herds/herds_view.html",
                {"form": form, "herd": herd, "herd_pub_id": herd_pub_id},
            )
    return render(
        request,
        "portal/herds/herds_view.html",
        {"form": form, "herd": herd, "herd_pub_id": herd_pub_id},
    )


#
# Animals
#


@login_required
def animals_list_view(request, herd_pub_id):
    herd = get_object_or_404(
        AnimalGroup, farm__users=request.user, public_id=herd_pub_id
    )
    animals = Animal.objects.filter(group=herd)
    return render(
        request,
        "portal/animals/animals_list.html",
        {"herd_pub_id": herd_pub_id, "animals": animals},
    )


@login_required
def animals_create_view(request, herd_pub_id):
    herd = get_object_or_404(
        AnimalGroup, farm__users=request.user, public_id=herd_pub_id
    )
    if request.method == "POST":
        form = AnimalForm(request.POST, request.FILES)
        if form.is_valid():
            new_animal = form.save(commit=False)
            new_animal.group = herd
            new_animal.farm = herd.farm
            new_animal.save()
            return redirect(
                reverse(
                    "portal:animals_detail_view",
                    kwargs={"animal_pub_id": new_animal.public_id},
                )
            )
        else:
            return render(
                request,
                "portal/animals/animals_create.html",
                {"form": form, "herd_pub_id": herd_pub_id},
            )
    else:
        form = AnimalForm()
        return render(
            request,
            "portal/animals/animals_create.html",
            {"form": form, "herd_pub_id": herd_pub_id},
        )


@login_required
def animals_detail_view(request, animal_pub_id):
    animal = get_object_or_404(Animal, public_id=animal_pub_id)
    form = AnimalForm(instance=animal)
    if request.method == "POST":
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            return redirect(
                reverse(
                    "portal:animals_detail_view",
                    kwargs={"animal_pub_id": animal.public_id},
                )
            )
        else:
            return render(
                request,
                "portal/animals/animals_view.html",
                {"form": form, "animal": animal},
            )
    return render(
        request,
        "portal/animals/animals_view.html",
        {"form": form, "animal": animal},
    )


#
# NFC Read and Write
#


@login_required
def tags_read_view(request):
    return render(request, "portal/nfc/nfc_read.html")


@login_required
def tags_write_view(request, animal_pub_id):
    animal = get_object_or_404(Animal, public_id=animal_pub_id)
    return render(request, "portal/nfc/tag_write_modal.html", {"tag_id": animal.tag_id})


#
# Utility Views
#


@login_required
def mass_create_animals_view(request, herd_pub_id):
    herd = get_object_or_404(
        AnimalGroup, farm__users=request.user, public_id=herd_pub_id
    )
    if request.method == "POST":
        form = MassAnimalForm(request.POST)
        if form.is_valid():
            try:
                with transaction.atomic():
                    for _ in range(form.cleaned_data["number_of_animals"]):
                        new_animal = Animal(
                            group=herd,
                            farm=herd.farm,
                            date_of_birth=form.cleaned_data["date_of_birth"],
                            category=form.cleaned_data["category"],
                            breed=form.cleaned_data["breed"],
                            sex=form.cleaned_data["sex"],
                        )
                        new_animal.save()
                    messages.success(
                        request,
                        f"Successfully created {form.cleaned_data['number_of_animals']} animals in herd {herd.name}.",
                    )
                    return render(
                        request,
                        "portal/animals/animals_create_mass.html",
                        {"form": MassAnimalForm(), "herd_pub_id": herd_pub_id},
                    )
            except Exception as e:
                messages.error(
                    request,
                    f"An error occurred while creating animals: {str(e)}",
                )
                return render(
                    request,
                    "portal/animals/animals_create_mass.html",
                    {"form": form, "herd_pub_id": herd_pub_id},
                )
        else:
            return render(
                request,
                "portal/animals/animals_create_mass.html",
                {"form": form, "herd_pub_id": herd_pub_id},
            )
    else:
        form = MassAnimalForm()
        return render(
            request,
            "portal/animals/animals_create_mass.html",
            {"form": form, "herd_pub_id": herd_pub_id},
        )
