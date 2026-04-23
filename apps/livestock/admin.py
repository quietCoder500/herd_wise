from typing import Any

from django.contrib import admin
from django.forms.models import ModelForm
from django.http import HttpRequest
from apps.livestock.models import Farm, AnimalGroup, Animal, ReportableModel
from polymorphic.admin import (
    PolymorphicChildModelAdmin,
    PolymorphicParentModelAdmin,
    PolymorphicChildModelFilter,
)


# Register your models here.


class ReportableModelChildAdmin(PolymorphicChildModelAdmin):
    """To be so for real I have no idea what this does..."""

    # base_model = <something maybe?>
    pass


@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ["name", "users_list", "public_id"]
    readonly_fields = ("public_id",)


@admin.register(AnimalGroup)
class AnimalGroupAdmin(ReportableModelChildAdmin):
    base_model = AnimalGroup
    show_in_index = True
    list_display = ["name", "farm__name", "public_id"]
    readonly_fields = ("public_id",)


@admin.register(Animal)
class AnimalAdmin(ReportableModelChildAdmin):
    base_model = Animal
    show_in_index = True
    fieldsets = [
        (
            None,
            {
                "fields": [
                    "name",
                    "group",
                    ("category", "breed"),
                    ("date_of_birth", "age"),
                    "date_of_death",
                ]
            },
        ),
        (
            "Advanced Options",
            {
                "classes": ["collapse"],
                "description": "Do not modify unless you know what you are doing!",
                "fields": ["group_index", "tag_id", "public_id", "id"],
            },
        ),
    ]
    readonly_fields = ("public_id", "id")
    list_display = ["formatted_name", "name", "group__name", "category", "public_id"]
    list_filter = ["category"]

    def get_form(
        self, request: HttpRequest, obj: Any | None = ..., *args, **kwargs: Any
    ) -> type[ModelForm]:
        form = super().get_form(request, obj, *args, **kwargs)
        try:
            form.base_fields["group_index"].required = False  # type: ignore
            if obj.date_of_death is not None:  # pyright: ignore[reportOptionalMemberAccess]
                form.base_fields["date_of_birth"].disabled = True  # pyright: ignore[reportAttributeAccessIssue]
                form.base_fields["age"].disabled = True  # pyright: ignore[reportAttributeAccessIssue]
        except AttributeError:
            pass
        return form


@admin.register(ReportableModel)
class ReportableModelParentAdmin(PolymorphicParentModelAdmin):
    """The parent model admin"""

    base_model = ReportableModel
    child_models = (Animal, AnimalGroup)  # type: ignore
    list_filter = (PolymorphicChildModelFilter,)
