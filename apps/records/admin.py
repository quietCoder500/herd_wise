from django.contrib import admin
from apps.records.models import Note, MedicalRecord, WeightRecord
# Register your models here.
@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    pass

@admin.register(MedicalRecord)
class MedicalRecordAdmin(admin.ModelAdmin):
    pass

@admin.register(WeightRecord)
class WeightRecordAdmin(admin.ModelAdmin):
    pass
