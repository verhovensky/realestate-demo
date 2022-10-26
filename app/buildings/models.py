from django.db import models
from django.core.validators import MinValueValidator

YANVMART = 1
APRILIYN = 2
IYLSEN = 3
OKTDEC = 4

QUARTERS = (
    (YANVMART, "Янв-март"),
    (APRILIYN, "Апрель-июнь"),
    (IYLSEN, "Июль-сентябрь"),
    (OKTDEC, "Октябрь-декабрь"),
    )


class Building(models.Model):

    name = models.CharField(verbose_name="Название",
                            max_length=255)
    year = models.IntegerField(validators=[
        MinValueValidator(2017)],
        verbose_name="Год постройки")
    quarter = models.PositiveSmallIntegerField(
        choices=QUARTERS,
        default=YANVMART,
        verbose_name="Квартал")
    builder = models.CharField(verbose_name="Застройщик",
                               max_length=255)
