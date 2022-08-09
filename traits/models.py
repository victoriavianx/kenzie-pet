from django.db import models

# Create your models here.
class Trait(models.Model):
    name = models.CharField(max_length=20, unique=True)

    animals = models.ManyToManyField(
        "animals.Animal", related_name="traits"
    )