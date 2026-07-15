from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db import transaction
from django.urls import reverse
from django.views import View
from django.shortcuts import get_list_or_404, get_object_or_404, redirect, render
from django.db.models import Q
from django.utils.text import slugify
from uuid import uuid4

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
                            kwargs={"slug": farm.slug},
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
                            kwargs={"slug": herd.slug},
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
                            kwargs={"slug": animal.slug},
                        ),
                    }
                )

            results.sort(key=lambda item: item["score"], reverse=True)

        context = {
            "results": results,
            "filters": {"farms": None, "herds": None, "record_types": None},
        }

        return AlpineTemplateResponse(request, "portal/search.html", context=context)


#
# Farms
#


@login_required
def farms_list_view(request):
    farms = Farm.objects.filter(users=request.user)
    return render(request, "portal/farms/farms_list.html", {"farms": farms})


@login_required
def farms_detail_view(request, slug):
    farm = get_object_or_404(Farm, slug=slug)
    form = FarmForm(instance=farm)
    return render(request, "portal/farms/farms_view.html", {"form": form, "farm": farm})


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
                    kwargs={"slug": new_farm.slug},
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
def herds_list_view(request, slug):
    farm = get_object_or_404(Farm, users=request.user, slug=slug)
    herds = AnimalGroup.objects.filter(farm=farm)
    return render(
        request,
        "portal/herds/herds_list.html",
        {"herds": herds, "farm": farm, "farm_slug": slug},
    )


@login_required
def herds_create_view(request, slug):
    farm = get_object_or_404(Farm, users=request.user, slug=slug)
    if request.method == "POST":
        form = HerdForm(request.POST)
        if form.is_valid():
            print("Valid form data:", form.cleaned_data)  # Debugging line
            new_herd = form.save(commit=False)
            new_herd.farm = farm
            new_herd.save()
            print(new_herd.name, new_herd.slug, str(new_herd))  # Debugging line
            messages.success(request, f"Successfully created herd {new_herd.name}.")
            return redirect(
                reverse(
                    "portal:herds_detail_view",
                    kwargs={"slug": new_herd.slug},
                )
            )
        else:
            return render(
                request,
                "portal/herds/herds_create.html",
                {"form": form, "farm_slug": farm.slug},
            )
    return render(
        request,
        "portal/herds/herds_create.html",
        {"form": HerdForm(), "farm_slug": farm.slug},
    )


@login_required
def herds_detail_view(request, slug):
    herd = get_object_or_404(AnimalGroup, slug=slug)
    form = HerdForm(instance=herd)
    if request.method == "POST":
        form = HerdForm(request.POST, instance=herd)
        if form.is_valid():
            form.save()
            messages.success(request, f"Successfully updated herd {herd.name}.")
            return redirect(
                reverse(
                    "portal:herds_detail_view",
                    kwargs={"slug": herd.slug},
                )
            )
        else:
            return render(
                request,
                "portal/herds/herds_view.html",
                {"form": form, "herd": herd, "herd_slug": slug},
            )
    return render(
        request,
        "portal/herds/herds_view.html",
        {"form": form, "herd": herd, "herd_slug": slug},
    )


#
# Animals
#


@login_required
def animals_list_view(request, slug):
    herd = get_object_or_404(AnimalGroup, farm__users=request.user, slug=slug)
    animals = Animal.objects.filter(group=herd)
    return render(
        request,
        "portal/animals/animals_list.html",
        {
            "herd_slug": slug,
            "herd": herd,
            "farm": herd.farm,
            "animals": animals,
        },
    )


@login_required
def animals_create_view(request, slug):
    herd = get_object_or_404(AnimalGroup, farm__users=request.user, slug=slug)
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
                    kwargs={"slug": new_animal.slug},
                )
            )
        else:
            return render(
                request,
                "portal/animals/animals_create.html",
                {"form": form, "herd_slug": slug},
            )
    else:
        form = AnimalForm()
        return render(
            request,
            "portal/animals/animals_create.html",
            {"form": form, "herd_slug": slug},
        )


@login_required
def animals_detail_view(request, slug):
    animal = get_object_or_404(Animal, slug=slug)
    form = AnimalForm(instance=animal)
    if request.method == "POST":
        form = AnimalForm(request.POST, request.FILES, instance=animal)
        if form.is_valid():
            form.save()
            return redirect(
                reverse(
                    "portal:animals_detail_view",
                    kwargs={"slug": animal.slug},
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
    templates = RecordTemplate.objects.filter(farm__users=request.user).order_by("name")

    if request.method == "POST":
        slug = request.POST.get("slug", "").strip()
        template_slug = request.POST.get("template_slug", "").strip()

        if not slug:
            messages.error(request, "Please read an NFC tag before continuing.")
        elif not template_slug:
            messages.error(request, "Please select a record form.")
        else:
            template = templates.filter(slug=template_slug).first()
            if template is None:
                messages.error(request, "Please select a valid record form.")
            else:
                return redirect(
                    reverse(
                        "portal:records_create_view",
                        kwargs={"slug": slug, "form_slug": template.slug},
                    )
                )

    return render(
        request,
        "portal/nfc/nfc_read.html",
        {"templates": templates},
    )


@login_required
def tags_write_view(request, slug):
    animal = get_object_or_404(Animal, slug=slug)
    return render(request, "portal/nfc/tag_write_modal.html", {"tag_id": animal.tag_id})


@login_required
def tags_link_redirect(request, slug):
    animal = get_object_or_404(Animal, slug=slug)
    forms = get_list_or_404(RecordTemplate, farm=animal.farm)
    return redirect(
        reverse(
            "portal:animal_records_create_view",
            kwargs={"slug": animal.slug, "form_slug": forms[0].slug},
        )
    )


#
# Record Views
#


class _RecordField:
    def __init__(
        self, name: str, label: str, data_type: str, required: bool, value
    ) -> None:
        self.name = name
        self.label = label
        self.data_type = data_type
        self.required = required
        self.value = value


@login_required
def all_records_list_view(request):
    records = LivestockRecord.objects.filter(report_link__farm__users=request.user)
    return render(request, "portal/records/records_list.html", {"records": records})


class RecordsCreateView(LoginRequiredMixin, View):
    def get(self, request, slug, form_slug):
        template = get_object_or_404(RecordTemplate, slug=form_slug)
        model_options = ReportableModel.objects.filter(farm__users=request.user)
        form = DynamicRecordForm(template=template, model_options=model_options)

        return render(
            request,
            "portal/records/records_create.html",
            {"form": form, "template": template, "slug": slug},
        )

    def post(self, request, slug, form_slug):
        template = get_object_or_404(RecordTemplate, slug=form_slug)
        model_options = ReportableModel.objects.filter(farm__users=request.user)
        form = DynamicRecordForm(
            request.POST, template=template, model_options=model_options
        )
        if form.is_valid():
            LivestockRecord.objects.create(
                report_link=get_object_or_404(
                    ReportableModel, farm__users=request.user, slug=slug
                ),
                template=template,
                data=form.cleaned_data,
            ).save()
            messages.success(request, "Record Created")

        return redirect(
            reverse(
                "portal:all_records_list_view",
            )
        )

    """render(
            request,
            "portal/records/records_create.html",
            {"form": form, "template": template, "slug": slug},
        )"""


class RecordsListView(LoginRequiredMixin, View):
    def get(self, request, slug):
        reportable_model = get_object_or_404(
            ReportableModel, farm__users=request.user, slug=slug
        )
        records = LivestockRecord.objects.filter(report_link=reportable_model)
        return render(
            request,
            "portal/records/records_list.html",
            {"records": records, "reportable_model": reportable_model},
        )


class RecordsDetailView(LoginRequiredMixin, View):
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
        return render(request, "portal/records/records_detail.html", context=context)


#
# Template Views
#


class TemplateCreateView(LoginRequiredMixin, View):
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
                        "name": slugify(form.cleaned_data.get("label", uuid4())),  # type: ignore
                        "label": form.cleaned_data.get("label"),
                        "field_type": form.cleaned_data.get("field_type", "text"),
                        "required": form.cleaned_data.get("required", True),
                    }
                )
            # For tomorrow me: Add another form using ModelForm for the RecordTemplate model's extra data
            # then create a validation for the schema, then save the model to the DB. Also, copy django's default form templates and add daisy UI to them.

        return render(request, "portal/add_record_template.html")


#
# Utility Views
#


@login_required
def mass_create_animals_view(request, slug):
    herd = get_object_or_404(AnimalGroup, farm__users=request.user, slug=slug)
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
                        {"form": MassAnimalForm(), "slug": slug},
                    )
            except Exception as e:
                messages.error(
                    request,
                    f"An error occurred while creating animals: {str(e)}",
                )
                return render(
                    request,
                    "portal/animals/animals_create_mass.html",
                    {"form": form, "slug": slug},
                )
        else:
            return render(
                request,
                "portal/animals/animals_create_mass.html",
                {"form": form, "slug": slug},
            )
    else:
        form = MassAnimalForm()
        return render(
            request,
            "portal/animals/animals_create_mass.html",
            {"form": form, "slug": slug},
        )
