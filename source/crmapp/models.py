from django.conf import settings
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _


class ExtraService(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name=_('Дополнительная услуга'))
    unit = models.CharField(max_length=350, null=True, blank=True, verbose_name=_('Единица измерения'))
    price = models.PositiveIntegerField(verbose_name=_('Цена'), null=False, blank=False)
    cleaning_time = models.IntegerField(verbose_name=_('Время уборки'), null=True, blank=True)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'extra_services'
        verbose_name = _('Дополнительная услуга')
        verbose_name_plural = _('Дополнительные услуги')


class ComplexityFactor(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False, verbose_name=_('Название коэффициента'))
    description = models.TextField(max_length=400, null=True, blank=True, verbose_name=_('Описание'))
    factor = models.DecimalField(max_digits=5, decimal_places=2, verbose_name=_('Значение коэффициента'))

    def __str__(self):
        return f'{self.name}-{self.factor}'

    class Meta:
        db_table = 'complexity_factor'
        verbose_name = _('Коэффициент сложности')
        verbose_name_plural = _('Коэффициенты сложности')


class CleaningSort(models.Model):
    name = models.CharField(max_length=200, verbose_name=_('Тип уборки'),
                            null=False, blank=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'cleaning_sort'
        verbose_name = _('Тип уборки')
        verbose_name_plural = _('Типы уборок')


UNIT_CHOICE = (
    ('Square meter', 'м²'),
    ('Piece', 'шт.')
)


class Service(models.Model):
    cleaning_sort = models.ForeignKey('crmapp.CleaningSort', on_delete=models.PROTECT,
                                      verbose_name=_('Тип уборки'),
                                      null=False, blank=False)
    property_sort = models.ForeignKey('crmapp.PropertySort', on_delete=models.PROTECT,
                                       verbose_name=_('Тип объекта'),
                                      null=False, blank=False)
    unit = models.CharField(max_length=125, verbose_name=_('Единица измерения'),
                            choices=UNIT_CHOICE, default='Square meter',
                            null=False, blank=False)
    price = models.PositiveIntegerField(verbose_name=_('Цена'), null=False, blank=False)

    def __str__(self):
        return f"{self.property_sort} {self.cleaning_sort} {self.price}"

    class Meta:
        db_table = 'service'
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')


class PropertySort(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Тип объекта'),
                            null=False, blank=False)

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = 'property_sort'
        verbose_name = _('Тип объекта')
        verbose_name_plural = _('Типы объектов')


class Client(models.Model):
    first_name = models.CharField(verbose_name=_('Имя'), max_length=75, blank=False, null=False)
    last_name = models.CharField(verbose_name=_('Фамилия'), max_length=75, blank=False, null=False)
    phone = PhoneNumberField(unique=True, region="KG", max_length=15, verbose_name=_('Номер телефона'))

    def __str__(self):
        return f"{self.first_name} {self.last_name} {self.phone}"

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = 'client'
        verbose_name = _('Клиент')
        verbose_name_plural = _('Клиенты')


class ForemanReport(models.Model):
    # Таблица для отчёта бригадира имеет связь FK с таблицей Order
    expenses = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Расходы'))
    start_at = models.DateTimeField(verbose_name=_('Дата и время начала работы'))
    end_at = models.DateTimeField(verbose_name=_('Дата и время окончания работы'))
    photo_before = models.ManyToManyField('crmapp.ForemanPhoto', null=True, blank=True, related_name='foreman_photo_before', verbose_name=_('Фото до начала работ'))
    photo_after = models.ManyToManyField('crmapp.ForemanPhoto', null=True, blank=True, related_name='foreman_photo_after', verbose_name=_('Фото после окончания работ'))

class ForemanPhoto(models.Model):
    # Таблица для хранения фотографий, имеет связь m2m с таблицей ForemanReport
    image = models.ImageField(upload_to='photo_obj', verbose_name=_('Фото'))

class ForemanOrderUpdate(models.Model):
    # Таблица для редактирования услуг и доп услуг в заказе для бригадира, имеет связь FK с таблицей Order
    service = models.ManyToManyField('crmapp.Service', null=True, blank=True, related_name='foreman_service', verbose_name=_('Услуга'))
    extra_service = models.ForeignKey('crmapp.ExtraService', on_delete=models.PROTECT, null=True, blank=True,
                                      related_name='foreman_extra', verbose_name=_('Дополнительная услуга'))

class Foreman(models.Model):
    # Таблица для выбора бригади в заказе, в которой указываем денежные моменты, имеет связь FK с таблицей Order
    staff = models.OneToOneField('accounts.Staff', related_name='foreman', on_delete=models.PROTECT, verbose_name=_('Бригадир'))
    bonus = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Бонус бригадира'))
    forfeit = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Штраф бригадира'))
    salary = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Зарплата'))

class Cleaners(models.Model):
    # Таблица для выбора клинеров в заказе, имеет связь m2m с таблицей order
    staff = models.OneToOneField('accounts.Staff', related_name='cleaner', on_delete=models.PROTECT,
                                 verbose_name=_('Клинер'))
    forfeit = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Штраф клинера'))
    salary = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Зарплата'))


class Order(models.Model): #Таблица самого заказа
    # Поле для сортировки незавершённых работ
    is_finished = models.BooleanField(default=False, verbose_name=_('Завершённая работа'))

    #Поля связанные со временем
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата и время создания заказа'))
    work_start = models.DateTimeField(verbose_name=_('Дата и время выполнения уборки'))
    work_time = models.TimeField(verbose_name=_('Время выполнения работ'))
    work_time_end = models.TimeField(verbose_name=_('Фактическое время выполнения работ'))

    #Информация о клиенте
    client_info = models.ForeignKey('crmapp.Client', on_delete=models.PROTECT, related_name='order_client', verbose_name=_('Информация клиента'))
    address = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Адрес'))

    #Уборки
    service = models.ManyToManyField('crmapp.Service',null=True, blank=True, related_name='order_service', verbose_name=_('Услуга'))
    extra_service = models.ForeignKey('crmapp.ExtraService', on_delete=models.PROTECT, null=True, blank=True,
                                      related_name='order_extra', verbose_name=_('Дополнительная услуга'))

    #Инвентарь для бригадира
    # inventory = models.ForeignKey()
    # soap_washer = models.ForeignKey()

    #Поля для Staff
    manager = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT, related_name='manager_order', verbose_name=_('Менеджер'))
    foreman = models.ForeignKey('crmapp.Foreman', on_delete=models.PROTECT, related_name='foreman_order', null=False,
                                blank=False, verbose_name=_('Бригадир заказа'))
    cleaners = models.ManyToManyField('crmapp.Cleaners', related_name='cleaners_order', verbose_name=_('Клинеры'))
    foremen_order = models.ForeignKey('crmapp.ForemanReport', on_delete=models.PROTECT, null=True, blank=True,
                                      verbose_name=_('Отчёт бригадира'))  #таблица для фото и доп расходов

    foreman_order_update = models.ForeignKey('crmapp.ForemanOrderUpdate', on_delete=models.PROTECT, null=True, blank=True,
                                             verbose_name=_('Редактирование услуг для бригадира')) #таблица для редактирования услуг для бригадира

    review = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)], verbose_name=_('Отзыв'))
    #Финансовая часть
    PAYMENT = (
        (0, _('Наличная оплата')),
        (1, _('Безналичная оплата'))
    )
    payment_type = models.CharField(max_length=100, null=False, blank=False, default=1, choices=PAYMENT, verbose_name=_('Вид оплаты'))             #вид оплаты
    total_cost = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Общая сумма заказа'))

    
    


class Inventory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Инвентарь'), null=False, blank=False)
    # datetime = models.DateTimeField(verbose_name=_('Дата и время'))
    # storage = models.CharField(max_length=255, verbose_name=_('Склад'))
    amount = models.IntegerField(verbose_name=_('Количество'), null=False, blank=False)


    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "inventory"
        verbose_name = _("Инвентарь")
        verbose_name_plural = _("Инвентари")


UNIT_CLEANSEARS_CHOICE = [
    ('Piece', 'штука'),
    ('Liter', 'литр'),
    ('kg', 'килограмм')
]


class Cleansear(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Моющее средство'), null=False, blank=False)
    description = models.TextField(max_length=510, verbose_name=_('Описание товара'), null=False, blank=False)
    unit = models.CharField(max_length=126, choices=UNIT_CLEANSEARS_CHOICE, default='Piece',
                            null=False, blank=False, verbose_name=_('Единица измерения'))
    price = models.PositiveIntegerField(verbose_name=_('Цена'), null=False, blank=False)
    amount = models.IntegerField(verbose_name=_('Количество'), null=False, blank=False)


    def __str__(self):
        return f"{self.name}:{self.price}"

    class Meta:
        db_table = "cleansear"
        verbose_name = _("Моющее средство")
        verbose_name_plural = _("Моющие средства")
