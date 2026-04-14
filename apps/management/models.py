from django.db import models
from django.utils.text import slugify
from django_extensions.db.fields import ShortUUIDField
from apps.users.models import User

import shortuuid
import uuid

class Farm(models.Model):
    name = models.CharField(verbose_name="name",max_length=100)
    public_id = ShortUUIDField(unique=True, editable=False, default=shortuuid.uuid)
    users = models.ManyToManyField(User)

    def users_list(self):
        return "\n".join([u.username for u in self.users.all()])

class AnimalGroup(models.Model):
    NAMING_SCHEMA = [
        ("CI", "<Animal Category> - <Animal Number>"),
        ("AN", "<Animal Name>"),
        ("BI", "<Animal Breed> - <Animal Number>")
    ]
    name = models.CharField(max_length=100)
    public_id = ShortUUIDField(unique=True, editable=False, default=shortuuid.uuid)
    farm = models.ForeignKey(Farm, on_delete=models.PROTECT, related_name="animal_groups")
    animal_naming_schema = models.CharField(max_length=2, choices=NAMING_SCHEMA)


        


class Animal(models.Model):
    ANIMAL_CATEGORY = [
        ("MC", "Market Chicken"),
        ("EC", "Exhibition Chicken"),
        ("ED", "Exhibition Duck"),
        ("MD", "Market Duck"),
        ("EG", "Exhibition Goose"),
        ("MG", "Market Goose"),
        ("ET", "Exhibition Turkey"),
        ("MT", "Market Turkey"),
        ("HGF", "Helmeted Guinea Fowl"),
        ("BS", "Breeding Swine"),
        ("MH", "Market Hog"),
        ("MB", "Market Beef"),
        ("MBF", "Beef, Feeder"),
        ("MDF", "Dairy Beef Feeder"),
        ("BB", "Beef, Breeder"),
        ("RB", "Rabbit, Breeder"),
        ("MR", "Market Rabbit"),
        ("RP", "Pet Rabbit"),
        ("DCF", "Dairy Calf"),
        ("DYH", "Dairy Yearling Heifer"),
        ("DC", "Dairy Cow"),
        ("DG", "Dairy Goat"),
        ("MG", "Market Goat"),
        ("SG", "Specialty Goat"),
        ("HO", "Horse"),
        ("LA", "Llama"),
        ("AL", "Alpaca"),
        ("ML", "Market Lamb"),
        ("BS", "Breed Sheep"),
    ]

    public_id = ShortUUIDField(unique=True, default=shortuuid.uuid)

    category = models.CharField(max_length=3, null=False, blank=False, choices=ANIMAL_CATEGORY)
    breed = models.CharField(max_length=200, null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    name = models.CharField(max_length=50, blank=True, null=True)
    tag_id = models.UUIDField(verbose_name="Tag UUID", unique=True, null=True, blank=True, default=uuid.uuid4)

    group = models.ForeignKey(AnimalGroup, verbose_name="Belongs to group: ", related_name="animals", on_delete=models.PROTECT)

