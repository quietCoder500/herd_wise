from django.db import models
from apps.users.models import User

class Farm(models.Model):
    users = models.ManyToManyField(User)

class AnimalGroup(models.Model):
    name = models.CharField(max_length=200)
    farm = models.ForeignKey(Farm, on_delete=models.PROTECT, related_name="animal_groups")

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
    category = models.CharField(max_length=3, null=False, blank=False, choices=ANIMAL_CATEGORY)
    breed = models.CharField(max_length=200, null=True, blank=True)

    date_of_birth = models.DateField(null=True, blank=True)
    age = models.IntegerField(null=True, blank= True)

    name = models.CharField(max_length=50, blank=True, null=True)
    tag_id = models.UUIDField(verbose_name="Tag UUID", unique=True, null=True, blank=True)

    group = models.ForeignKey(AnimalGroup, verbose_name="Belongs to group: ", related_name="animals", on_delete=models.PROTECT)

