from django.db import models

# Create your models here.


class ExtraService(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name="Дополнительная услуга")
    unit = models.CharField(max_length=350, null=True, blank=True, verbose_name="Единица измерения")
    price = models.PositiveIntegerField(verbose_name="Цена", null=False, blank=False)
    cleaning_time = models.CharField(max_length=255, verbose_name="Время уборки", null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'extra_services'
        verbose_name = 'extra_service'
        verbose_name_plural = 'extra_services'