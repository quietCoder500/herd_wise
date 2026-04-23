from django.db import models
from django.utils.text import slugify
from apps.livestock.models import Animal, ReportableModel
from apps.users.models import User


# Create your models here.
class Note(models.Model):
    record_link = models.ForeignKey(
        ReportableModel, on_delete=models.PROTECT
    )  # Maybe needs to be preserved...
    title = models.CharField(max_length=70)
    body = models.TextField()
    slug = models.SlugField(unique=True)
    created_on = models.DateTimeField(auto_now=False, auto_now_add=False)
    updated_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(
        User, on_delete=models.RESTRICT
    )  # I think restrict is appropriate here?

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.title)
        super(Note, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'Note "{self.title}"'


class MedicalRecord(models.Model):
    record_link = models.ForeignKey(
        ReportableModel, on_delete=models.PROTECT
    )  # MEDICAL RECORDS MUST BE PROTECTED FROM DELETION


class WeightRecord(models.Model):
    animal = models.ForeignKey(
        Animal, on_delete=models.CASCADE
    )  # These can probably be deleted...
    created_on = models.DateTimeField(auto_now=False, auto_now_add=True)
    weight_in_kg = models.FloatField()

    def __str__(self) -> str:
        return f'"{self.animal.formatted_name}" Weight record entry'
