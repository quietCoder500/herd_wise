from django.db import models
from apps.livestock.models import Animal, AnimalGroup

# Create your models here.
class Note(models.Model):
    # This would relate to animals and animal groups
    pass

class MedicalRecord(models.Model):
    # This may relate to animals and animal groups
    pass

class WeightRecord(models.Model):
    # This will relate to only animals
    pass
