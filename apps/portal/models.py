import uuid
from datetime import date

import shortuuid
from dateutil.relativedelta import relativedelta
from django.db import models
from django_extensions.db.fields import ShortUUIDField
from polymorphic.models import PolymorphicModel

from apps.users.models import User


def gen_name_from_schema(obj, schema: str) -> str:
    if schema == "IC":
        return f"No. {obj.group_index} - {obj.get_category_display()}"
    elif schema == "AN":
        return f"{obj.name}"
    elif schema == "BI":
        return f"{obj.breed} - {obj.group_index}"
    raise ValueError(
        f'Animal group naming schema ID, "{schema}", is not a valid Animal naming schema'
    )


def get_age(date_of_birth):
    today = date.today()
    diff = relativedelta(today, date_of_birth)
    return diff.years


class Farm(models.Model):
    name = models.CharField(verbose_name="name", max_length=100)
    public_id = ShortUUIDField(unique=True, editable=False, default=shortuuid.uuid)
    users = models.ManyToManyField(User, related_name="farms")
    photo = models.ImageField(upload_to="farm_photos/", null=True, blank=True)
    location = models.CharField(
        verbose_name="Location Name or Address", max_length=255, null=True, blank=True
    )

    def users_list(self) -> str:
        return "\n".join([u.username + ", " for u in self.users.all()]).rstrip(", ")

    def __str__(self) -> str:
        return self.name  # pyright: ignore[reportReturnType]


class ReportableModel(PolymorphicModel):
    # This is a abstract model that allows for the records app
    # to reference Animal or AnimalGroup from one model relation.
    farm = models.ForeignKey(
        Farm, on_delete=models.PROTECT, related_name="animal_groups"
    )

    def __str__(self) -> str:
        return str(self.get_real_instance())


class AnimalGroup(ReportableModel):
    NAMING_SCHEMA = [
        ("IC", "<Animal Number> - <Animal Category>"),
        ("AN", "<Animal Name>"),
        ("BI", "<Animal Breed> - <Animal Number>"),
    ]
    name = models.CharField(max_length=100)
    public_id = ShortUUIDField(unique=True, editable=False, default=shortuuid.uuid)
    animal_naming_schema = models.CharField(
        max_length=2, choices=NAMING_SCHEMA, default="IC"
    )

    def __str__(self) -> str:
        return str(self.name)


class Animal(ReportableModel):
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
    public_id = ShortUUIDField(unique=True, default=shortuuid.uuid, editable=False)

    category = models.CharField(
        max_length=3, null=False, blank=False, choices=ANIMAL_CATEGORY
    )
    breed = models.CharField(max_length=200, null=True, blank=True)

    date_of_birth = models.DateField(
        "Date of Birth (Priority over age value)", null=True, blank=True
    )
    date_of_death = models.DateField("Date of Death", null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)

    name = models.CharField(max_length=50, blank=True, null=True)
    tag_id = models.UUIDField(
        verbose_name="Tag UUID", unique=True, null=True, blank=True, default=uuid.uuid4
    )

    group = models.ForeignKey(
        AnimalGroup,
        verbose_name="Belongs to group: ",
        related_name="animals",
        on_delete=models.PROTECT,
    )
    group_index = models.SmallIntegerField("The animal's id within its group")

    @property
    def formatted_name(self):
        return gen_name_from_schema(self, self.group.animal_naming_schema)

    def get_current_age(self):
        if self.date_of_birth is not None:
            dob_age = get_age(self.date_of_birth)
            if self.age is not None:
                if self.age == dob_age:
                    return dob_age
                elif self.age > dob_age:
                    raise ValueError("Set animal age is higher than the age from DoB")
                elif self.age < dob_age:
                    self.age = dob_age
                    self.save()
                    return dob_age
            else:
                self.age = dob_age
                self.save()
                return dob_age
        else:
            return self.age

    def __str__(self) -> str:
        return self.formatted_name

    def save(self, *args, **kwargs) -> None:
        # Below runs on first save
        if not self.id:  # pyright: ignore[reportAttributeAccessIssue]
            # Incrementing logic for group_index
            largest = (
                Animal.objects.filter(group=self.group).order_by("group_index").last()
            )
            if not largest:
                self.group_index = 1
            else:
                self.group_index = largest.group_index + 1

        # Below runs on all saves
        # Age calculation logic
        if self.date_of_birth is not None:
            self.age = self.get_current_age()

        return super(Animal, self).save(*args, **kwargs)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["group", "group_index"], name="unique_index_within_group"
            )
        ]


class RecordTemplate(models.Model):
    """
    Schema definition model

    Valid syntax:
    [ # each list item is a form element
        {
            "name": name,
            "label": label,
            "field_type": type,
            "required": required
        },
    ]

    name: str
    label: str
    field_type: str Options["number", "date", "boolean", "char", "text"]
    """

    farm = models.ForeignKey(
        Farm, on_delete=models.CASCADE, related_name="record_templates"
    )
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100)
    description = models.TextField(blank=True)
    schema = models.JSONField()

    def __str__(self) -> str:
        return self.name

    class Meta:
        unique_together = ("slug", "farm")


class LivestockRecord(models.Model):
    public_id = models.UUIDField(default=uuid.uuid4, editable=False)
    report_link = models.ForeignKey(ReportableModel, on_delete=models.CASCADE)
    template = models.ForeignKey(RecordTemplate, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    data = models.JSONField()

    def __str__(self) -> str:
        return f"{self.template.name} Record for {self.report_link}"
