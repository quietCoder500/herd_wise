from django.contrib import admin
from apps.records.models import Note, MedicalRecord, WeightRecord


# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ["slug", "record_link", "user", "created_on", "updated_on"]
    prepopulated_fields = {"slug": ("title",)}


@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    pass


@admin.register(WeightRecord)
class WeightRecordAdmin(admin.ModelAdmin):
    list_display = ["animal", "created_on"]
