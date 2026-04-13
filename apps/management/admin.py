from django.contrib import admin
from apps.management.models import Farm, AnimalGroup, Animal

# Register your models here.
@admin.register(Farm)
class FarmAdmin(admin.ModelAdmin):
    pass

@admin.register(AnimalGroup)
class AnimalGroupAdmin(admin.ModelAdmin):
    pass

@admin.register(Animal)
class AnimalAdmin(admin.ModelAdmin):
    pass

