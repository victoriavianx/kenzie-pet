from django.db import models

# Create your models here.
class CategorySex(models.TextChoices):
    FEMEA = "Fêmea"
    MACHO = "Macho"
    NAO_INFORMADO = "Não informado"

class Animal(models.Model):
    name = models.CharField(max_length=50)
    age = models.IntegerField(null=False)
    weight = models.FloatField(null=False)
    sex = models.CharField(
        max_length=15,
        choices=CategorySex.choices,
        default=CategorySex.NAO_INFORMADO
    )

    group = models.ForeignKey(
        "groups.Group",
        on_delete=models.CASCADE,
        related_name="animals"
    )