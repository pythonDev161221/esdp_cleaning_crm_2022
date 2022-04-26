from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _

from crmapp.choice import PaymentChoices, UnitChoices, UnitCleansearsChoice


class BaseService(models.Model):
    amount = models.IntegerField(verbose_name=_('Объем работы'), null=False, blank=False)
    rate = models.DecimalField(default=1, null=False, blank=False, verbose_name=_('Коэффицент сложности'),
                               max_digits=2, decimal_places=1,
                               validators=[MinValueValidator(1.0), MaxValueValidator(3.0)])
    total = models.PositiveIntegerField(null=False, blank=False, verbose_name=_('Стоимость доп. услуги'))


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


class Service(models.Model):
    cleaning_sort = models.ForeignKey('crmapp.CleaningSort', on_delete=models.PROTECT,
                                      related_name='service_cleaning',
                                      verbose_name=_('Тип уборки'),
                                      null=False, blank=False)
    property_sort = models.ForeignKey('crmapp.PropertySort', on_delete=models.PROTECT,
                                      related_name='service_property',
                                      verbose_name=_('Тип объекта'),
                                      null=False, blank=False)
    unit = models.CharField(max_length=125, verbose_name=_('Единица измерения'),
                            choices=UnitChoices.choices, default='square_meter',
                            null=False, blank=False)
    price = models.PositiveIntegerField(verbose_name=_('Цена'), null=False, blank=False)

    def __str__(self):
        return f"{self.property_sort} {self.cleaning_sort} {self.price}сом за {self.unit}"

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

    def get_absolute_url(self):
        return reverse('crmapp:client_index')

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
    order = models.ForeignKey('crmapp.Order', on_delete=models.PROTECT, null=False, blank=False,
                              related_name='foreman_order_report', verbose_name=_('Заказ'))
    expenses = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Расходы'))
    start_at = models.DateTimeField(verbose_name=_('Дата и время начала работы'))
    end_at = models.DateTimeField(verbose_name=_('Дата и время окончания работы'))
    photo_before = models.ManyToManyField('crmapp.ForemanPhoto',
                                          related_name='foreman_photo_before', verbose_name=_('Фото до начала работ'))
    photo_after = models.ManyToManyField('crmapp.ForemanPhoto',
                                         related_name='foreman_photo_after',
                                         verbose_name=_('Фото после окончания работ'))


class ForemanPhoto(models.Model):
    # Таблица для хранения фотографий, имеет связь m2m с таблицей ForemanReport
    image = models.ImageField(upload_to='photo_obj', verbose_name=_('Фото'))


class ForemanOrderUpdate(models.Model):
    # Таблица для редактирования услуг и доп услуг в заказе для бригадира, имеет связь FK с таблицей Order
    order = models.ForeignKey('crmapp.Order', on_delete=models.PROTECT, null=False, blank=False,
                              related_name='foreman_order_update', verbose_name=_('Заказ'))
    updated_services = models.ManyToManyField('crmapp.ServiceOrder', related_name='foreman_orders_update',
                                              verbose_name=_('Обновляемая Услуга'),
                                              through='crmapp.ServiceForemanOrderUpdate',
                                              through_fields=('foreman_order_update', 'service_updated'))
    updated_extra_services = models.ManyToManyField('crmapp.ExtraServiceOrder',
                                                    related_name='foreman_orders_update',
                                                    verbose_name=_('Обновляемая дополнительная услуга'),
                                                    through='crmapp.ExtraServiceForemanOrderUpdate',
                                                    through_fields=('foreman_order_update', 'extra_service_updated'))
    added_services = models.ManyToManyField('crmapp.Service', related_name='foreman_orders_add',
                                            verbose_name=_('Добавляемая Услуга'),
                                            through='crmapp.ServiceForemanOrderAdd',
                                            through_fields=('foreman_order_update', 'service_added'))
    added_extra_services = models.ManyToManyField('crmapp.ExtraService',
                                                  related_name='foreman_orders_add',
                                                  verbose_name=_('Добавляемая дополнительная услуга'),
                                                  through='crmapp.ExtraServiceForemanOrderAdd',
                                                  through_fields=('foreman_order_update', 'extra_service_added'))


class StaffOrder(models.Model):
    order = models.ForeignKey('crmapp.Order', related_name='order_cliners', verbose_name=_('Заказ'), null=False,
                              blank=False, on_delete=models.PROTECT)
    staff = models.ForeignKey(get_user_model(), related_name='cliner_orders', verbose_name=_('Клинер'),
                              null=False, blank=False, on_delete=models.PROTECT)
    is_brigadier = models.BooleanField(verbose_name=_('Бригадир'), default=False)


class Order(models.Model):  # Таблица самого заказа
    # Поле для сортировки незавершённых работ
    is_finished = models.BooleanField(default=False, verbose_name=_('Завершённая работа'))

    # Поля связанные со временем
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата и время создания заказа'))
    work_start = models.DateTimeField(verbose_name=_('Дата и время выполнения уборки'))
    work_time = models.TimeField(verbose_name=_('Время выполнения работ'))

    # Информация о клиенте
    client_info = models.ForeignKey('crmapp.Client', on_delete=models.PROTECT, related_name='order_client',
                                    verbose_name=_('Информация клиента'))
    address = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Адрес'))

    # Уборки
    services = models.ManyToManyField('crmapp.Service', related_name='orders',
                                      verbose_name=_('Услуга'), through='crmapp.ServiceOrder',
                                      through_fields=('order', 'service'))
    extra_services = models.ManyToManyField('crmapp.ExtraService',
                                            related_name='orders', verbose_name=_('Дополнительная услуга'),
                                            through='crmapp.ExtraServiceOrder',
                                            through_fields=('order', 'extra_service'))

    # Поля для Staff
    manager = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='manager_order',
                                verbose_name=_('Менеджер'))
    cleaners = models.ManyToManyField(get_user_model(), related_name='orders', verbose_name=_('Клинер'),
                                      through='crmapp.StaffOrder',
                                      through_fields=('order', 'staff'))

    review = models.PositiveIntegerField(null=True, blank=True, validators=[MinValueValidator(1), MaxValueValidator(5)],
                                         verbose_name=_('Отзыв'))
    # Финансовая часть
    payment_type = models.CharField(max_length=25, null=False, blank=False, default='cash',
                                    choices=PaymentChoices.choices,
                                    verbose_name=_('Вид оплаты'))  # вид оплаты
    total_cost = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Общая сумма заказа'))


class FineCategory(models.Model):
    name = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Категория'))

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'fine_category'
        verbose_name = _('Категория для штрафа')
        verbose_name_plural = _('Категории для штрафа')


class Fine(models.Model):
    category = models.ForeignKey('crmapp.FineCategory', on_delete=models.PROTECT, null=True, blank=True,
                                 related_name='fines', verbose_name=_('Категория'))
    fine = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('Штраф'))
    criteria = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Критерий'))
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Сумма штрафа'))
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('Пояснение'))

    def __str__(self):
        return f"{self.fine} - {self.value}"

    class Meta:
        db_table = 'fine'
        verbose_name = _('Штраф')
        verbose_name_plural = _('Штрафы')


class Bonus(models.Model):
    bonus = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('Бонус'))
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Сумма бонуса'))

    def __str__(self):
        return f"{self.bonus} - {self.value}"

    class Meta:
        db_table = 'bonus'
        verbose_name = _('Бонус')
        verbose_name_plural = _('Бонусы')


class Inventory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Инвентарь'), null=False, blank=False)
    amount = models.IntegerField(verbose_name=_('Количество'), null=False, blank=False)

    def get_absolute_url(self):
        return reverse('crmapp:inventory_index')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "inventory"
        verbose_name = _("Инвентарь")
        verbose_name_plural = _("Инвентари")


class Cleansear(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Моющее средство'), null=False, blank=False)
    description = models.TextField(max_length=510, verbose_name=_('Описание товара'), null=False, blank=False)
    unit = models.CharField(max_length=126, choices=UnitCleansearsChoice.choices, default='Piece',
                            null=False, blank=False, verbose_name=_('Единица измерения'))
    price = models.PositiveIntegerField(verbose_name=_('Цена'), null=False, blank=False)
    amount = models.IntegerField(verbose_name=_('Количество'), null=False, blank=False)

    def get_absolute_url(self):
        return reverse('crmapp:cleansear_index')

    def __str__(self):
        return f"{self.name}:{self.price}"

    class Meta:
        db_table = "cleansear"
        verbose_name = _("Моющее средство")
        verbose_name_plural = _("Моющие средства")


class ServiceForemanOrderUpdate(BaseService):
    foreman_order_update = models.ForeignKey('crmapp.ForemanOrderUpdate', related_name='foreman_order_update_services',
                                             verbose_name='Обновленный заказ', null=False, blank=False,
                                             on_delete=models.PROTECT)
    service_updated = models.ForeignKey('crmapp.ServiceOrder', related_name='service_updated',
                                        verbose_name='Обновляемая услуга', null=False, blank=False,
                                        on_delete=models.PROTECT)
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('Причина внесения изменений'))

    def __str__(self):
        return f"{self.service_updated}: {self.total}"

    class Meta:
        db_table = "service_update"
        verbose_name = _("Обновленная услуга заказа")
        verbose_name_plural = _("Обновленные услуги заказа")


class ExtraServiceForemanOrderUpdate(BaseService):
    foreman_order_update = models.ForeignKey('crmapp.ForemanOrderUpdate',
                                             related_name='foreman_order_update_extra_services',
                                             verbose_name='Обновленный заказ', null=False, blank=False,
                                             on_delete=models.PROTECT)
    extra_service_updated = models.ForeignKey('crmapp.ExtraServiceOrder', related_name='extra_service_updated_orders',
                                              verbose_name=_('Доп. услуга'), null=False, blank=False,
                                              on_delete=models.PROTECT)
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('Причина внесения изменений'))

    def __str__(self):
        return f"{self.extra_service_updated}: {self.total}"

    class Meta:
        db_table = "extra_service_update"
        verbose_name = _("Обновленная доп. услуга заказа")
        verbose_name_plural = _("Обновленные доп. услуги заказа")


class ServiceForemanOrderAdd(BaseService):
    foreman_order_update = models.ForeignKey('crmapp.ForemanOrderUpdate', related_name='foreman_order_services',
                                             verbose_name=_('Заказ'),
                                             null=False, blank=False, on_delete=models.PROTECT)
    service_added = models.ForeignKey('crmapp.Service', related_name='service_foreman_orders', verbose_name=_('Услуга'),
                                      null=False, blank=False, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.service_added}: {self.total}"

    class Meta:
        db_table = "service_added"
        verbose_name = _("Добавленная услуга заказа")
        verbose_name_plural = _("Добавленные услуги заказа")


class ExtraServiceForemanOrderAdd(BaseService):
    foreman_order_update = models.ForeignKey('crmapp.ForemanOrderUpdate', related_name='foreman_order_extra_services',
                                             verbose_name=_('Заказ'), null=False,
                                             blank=False,
                                             on_delete=models.PROTECT)
    extra_service_added = models.ForeignKey('crmapp.ExtraService', related_name='extra_service_foreman_orders',
                                            verbose_name=_('Доп. услуга'),
                                            null=False, blank=False, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.extra_service_added}: {self.total}"

    class Meta:
        db_table = "extra_service_added"
        verbose_name = _("Добавленная доп. услуга заказа")
        verbose_name_plural = _("Добавленные доп. услуги заказа")


class ServiceOrder(BaseService):
    order = models.ForeignKey('crmapp.Order', related_name='order_services', verbose_name=_('Заказ'), null=False,
                              blank=False, on_delete=models.PROTECT)
    service = models.ForeignKey('crmapp.Service', related_name='service_orders', verbose_name=_('Услуга'),
                                null=False, blank=False, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.service}: {self.total}"

    class Meta:
        db_table = "service_order"
        verbose_name = _("Услуга заказа")
        verbose_name_plural = _("Услуги заказа")


class ExtraServiceOrder(BaseService):
    order = models.ForeignKey('crmapp.Order', related_name='order_extra_services', verbose_name=_('Заказ'), null=False,
                              blank=False, on_delete=models.PROTECT)
    extra_service = models.ForeignKey('crmapp.ExtraService', related_name='extra_service_orders',
                                      verbose_name=_('Доп. услуга'), null=False, blank=False, on_delete=models.PROTECT)

    def __str__(self):
        return f"{self.extra_service}: {self.total}"

    class Meta:
        db_table = "extra_service_order"
        verbose_name = _("Доп. услуга заказа")
        verbose_name_plural = _("Доп. услуги заказа")
