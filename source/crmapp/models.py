from django.db import models
from django.contrib.postgres.fields import ArrayField


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


class ComplexityFactor(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name="Коэффициент сложности")
    description = models.TextField(max_length=400, null=True, blank=True, verbose_name="Описание")
    factor = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return f'{self.name}-{self.factor}'

    class Meta:
        db_table = 'complexity_factor'
        verbose_name = 'complexity_factor'
        verbose_name_plural = 'complexity_factors'


class TypeOfCleaning(models.Model):
    cleaning_type = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return f"{self.cleaning_type}"


class TypeOfObjectAndClean(models.Model):
    object_to_clean = models.ForeignKey('crmapp.TypeOfObject', on_delete=models.CASCADE)
    cleaning = models.ForeignKey(TypeOfCleaning, on_delete=models.CASCADE)
    price = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.cleaning} {self.object_to_clean} {self.price}"


class TypeOfObject(models.Model):
    object_type = models.CharField(max_length=200, null=False, blank=False)
    cleanings = models.ManyToManyField(TypeOfCleaning, through=TypeOfObjectAndClean,
                                       related_name='type_of_objects')

    def __str__(self):
        return f"{self.object_type}"


class Client(models.Model):
    first_name = models.CharField(verbose_name='Имя', max_length=75, blank=False, null=False)
    last_name = models.CharField(verbose_name='Фамилия', max_length=75, blank=False, null=False)
    # поле phone CharField требуется валидатор для проверки минимального количества символов в номере
    phone = ArrayField(models.CharField(max_length=20, verbose_name='Номер телефона'))
    # поле is_constant требуется уточнение у заказчика
    #is_constant = models.BooleanField(default=False, verbose_name='Статус клиента',)

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "client"
        verbose_name = "Клиент"
        verbose_name_plural = "Клиенты"

