from django.contrib import admin
from apps.management.models import Farm, AnimalGroup, Animal

# Register your models here.
@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    list_display = ["name", "users_list", "public_id"]
    readonly_fields = ("public_id",)

@admin.register(AnimalGroup)
class AnimalGroupAdmin(admin.ModelAdmin):
    list_display = ["name", "farm__name", "public_id"]
    readonly_fields = ("public_id",)

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    fieldsets = [
        (
            None, 
            {
                "fields": ["name", "group", ("category", "breed"), ("date_of_birth", "age")]
            }
        ),
        (
            "Advanced Options",
            {
                "classes": ["collapse"],
                "description": "Do not modify unless you know what you are doing!",
                "fields": ["tag_id", "public_id", "id"]
            }
        )
    ]
    readonly_fields = ("public_id", "id")
    list_display = ["formatted_name", "name", "group__name", "category", "public_id"]
    list_filter = ["category"]
