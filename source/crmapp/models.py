from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.http import QueryDict

from django.urls import reverse
from phonenumber_field.modelfields import PhoneNumberField
from django.utils.translation import gettext as _

from crmapp.choice import PaymentChoices, UnitChoices, OrderStatusChoices, PartUnits
from crmapp.constants import ORDER_STAFF_SALARY_COEFFICIENT


class Service(models.Model):
    name = models.CharField(max_length=300, null=False, blank=False, verbose_name=_('Услуга'))
    unit = models.CharField(max_length=350, null=False, blank=False, choices=UnitChoices.choices,
                            verbose_name=_('Единица измерения'), default='square_meter')
    price = models.PositiveIntegerField(verbose_name=_('Цена за единицу'), null=False, blank=False)
    is_extra = models.BooleanField(verbose_name=_('Доп. услуга'))

    def get_field_value(self, field_name):
        if field_name == 'unit':
            return self.get_unit_display()
        return getattr(self, field_name)

    def __iter__(self):
        for field in self._meta.fields:
            yield field.verbose_name, self.get_field_value(field.name)

    def __str__(self):
        return f'{self.name}'

    class Meta:
        db_table = 'service'
        verbose_name = _('Услуга')
        verbose_name_plural = _('Услуги')


class Client(models.Model):
    first_name = models.CharField(verbose_name=_('Имя'), max_length=75, blank=False, null=False)
    last_name = models.CharField(verbose_name=_('Фамилия'), max_length=75, blank=False, null=False)
    phone = PhoneNumberField(unique=True, region="KG", max_length=15, verbose_name=_('Номер телефона'))
    organization = models.CharField(verbose_name=_('Организация'), max_length=120, null=True, blank=True)

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


class ForemanExpenses(models.Model):
    amount = models.PositiveIntegerField(null=True, blank=True, default=0, verbose_name=_('Сумма расхода'))
    description = models.TextField(max_length=1000, null=True, blank=True, verbose_name=_('Описание расхода'))
    foreman_report = models.ForeignKey('crmapp.StaffOrder', on_delete=models.CASCADE, null=False, blank=False,
                                       related_name='foreman_expense', verbose_name=_('Отчёт бригадира'))

    db_table = 'foreman_expense'
    verbose_name = _('Расход бригадира')
    verbose_name_plural = _('Расходы бригадира')


class ForemanPhoto(models.Model):
    foreman_report = models.ForeignKey('crmapp.StaffOrder', null=False, blank=False, on_delete=models.CASCADE,
                                       related_name='foreman_photo', verbose_name='Фото до начала работ')
    is_after = models.BooleanField(default=False, verbose_name='Фото после окончания работ')
    image = models.ImageField(upload_to='photo_foreman/', verbose_name=_('Фото'))

    class Meta:
        db_table = 'foreman_photo'
        verbose_name = _('Фотография от бригадира')
        verbose_name_plural = _('Фотографии от бригадира')


class ForemanOrderUpdate(models.Model):
    order = models.ForeignKey('crmapp.Order', on_delete=models.PROTECT, null=False, blank=False,
                              related_name='foreman_order_update', verbose_name=_('Заказ'))
    services = models.ManyToManyField('crmapp.ServiceOrder', related_name='foreman_order_update',
                                      verbose_name=_('Услуга'))

    class Meta:
        db_table = 'foreman_order_update'
        verbose_name = _('Корректировка бригадира')
        verbose_name_plural = _('Корректировки бригадиров')


class StaffOrder(models.Model):
    order = models.ForeignKey('crmapp.Order', related_name='order_cleaners', verbose_name=_('Заказ'), null=False,
                              blank=False, on_delete=models.PROTECT)
    staff = models.ForeignKey(get_user_model(), related_name='cleaner_orders', verbose_name=_('Клинер'),
                              null=False, blank=False, on_delete=models.PROTECT)
    is_brigadier = models.BooleanField(verbose_name=_('Бригадир'), default=False)
    is_accept = models.BooleanField(null=True, blank=True, default=False, verbose_name=_('Принял заказ'))
    is_refuse = models.BooleanField(null=True, blank=True, default=False, verbose_name=_('Отказался от заказа'))
    in_place = models.DateTimeField(null=True, blank=True, verbose_name=_('Время прибытия на заказ'))
    work_start = models.DateTimeField(null=True, blank=True, verbose_name=_('Начало работ'))
    work_end = models.DateTimeField(null=True, blank=True, verbose_name=_('Конец работ'))

    class Meta:
        db_table = 'staff_order'
        verbose_name = _('Сотрудник в заказе')
        verbose_name_plural = _('Сотрудники в заказе')

    def get_total_expenses(self):
        total = 0
        for expense in self.foreman_expense.all():
            total += expense.amount
        return total


class Order(models.Model):
    status = models.CharField(max_length=50, default='new', verbose_name=_('Статус заказа'),
                              choices=OrderStatusChoices.choices, null=True, blank=True)
    object_type = models.ForeignKey('crmapp.ObjectType', on_delete=models.PROTECT, related_name='orders',
                                    verbose_name=_('Тип объекта'), null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True, verbose_name=_('Дата и время создания заказа'))
    work_start = models.DateTimeField(verbose_name=_('Дата и время начала уборки'), null=True, blank=True)
    cleaning_time = models.DurationField(verbose_name=_('Время выполнения работ'), null=True, blank=True)
    work_end = models.DateTimeField(null=True, blank=True, verbose_name=_('Дата и время окончания уборки'))
    client_info = models.ForeignKey('crmapp.Client', on_delete=models.PROTECT, related_name='order_client',
                                    verbose_name=_('Информация клиента'))
    address = models.CharField(max_length=256, null=False, blank=False, verbose_name=_('Адрес'))
    services = models.ManyToManyField('crmapp.Service', related_name='orders',
                                      verbose_name=_('Услуга'), through='crmapp.ServiceOrder',
                                      through_fields=('order', 'service'))
    manager = models.ForeignKey(get_user_model(), on_delete=models.PROTECT, related_name='manager_order',
                                verbose_name=_('Менеджер'))
    cleaners = models.ManyToManyField(get_user_model(), related_name='orders', verbose_name=_('Клинер'),
                                      through='crmapp.StaffOrder',
                                      through_fields=('order', 'staff'))

    review = models.PositiveIntegerField(null=True, blank=True,
                                         validators=[MinValueValidator(1), MaxValueValidator(5)],
                                         verbose_name=_('Отзыв'))
    payment_type = models.CharField(max_length=25, null=False, blank=False, default='cash',
                                    choices=PaymentChoices.choices,
                                    verbose_name=_('Вид оплаты'))
    cleaners_part = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Доля клинеров'))

    part_units = models.CharField(max_length=25, null=False, blank=False, default='som', choices=PartUnits.choices,
                                  verbose_name=_('Способ расчета'))

    inventories = models.ManyToManyField("crmapp.Inventory", related_name='order_inventories',
                                         verbose_name=_('Инвентарь'),
                                         through='crmapp.InventoryOrder'),
    description = models.TextField(max_length=2000, null=True, blank=False, verbose_name=_('Примечание'))
    is_deleted = models.BooleanField(null=True, blank=True, default=False, verbose_name=_('Удален'))

    def finish_order(self):
        self.status = 'finished'
        self.save()

    def cancel_order(self):
        self.status = 'canceled'
        self.save()

    def soft_delete(self):
        self.is_deleted = True
        self.save()

    def get_all_staff_expenses(self):
        expenses = 0
        for expense in self.order_manager.all():
            expenses += expense.get_salary()
        return expenses

    def get_foreman_expenses(self):
        if self.order_cleaners:
            for report in self.order_cleaners.all():
                return report.get_total_expenses()
        return 0

    def get_income_outcome(self):
        return self.get_total() - self.get_all_staff_expenses() - self.get_foreman_expenses()

    def manager_report_base_sum(self, staff_is_accept_order):
        staff_part = int(
            self.cleaners_part) / staff_is_accept_order.count()
        base_sum = 0
        for order_staff in staff_is_accept_order:
            for coefficient in ORDER_STAFF_SALARY_COEFFICIENT:
                if str(order_staff.staff.experience) == coefficient[0]:
                    base_sum += staff_part * coefficient[1]
        return base_sum

    def manager_report_numeric_coefficient(self, staff_is_accept_order):
        staff_part = int(
            self.cleaners_part) / staff_is_accept_order.count()
        base_num = self.manager_report_base_sum(staff_is_accept_order)
        num_coefficient = []
        for order_staff in staff_is_accept_order:
            for coefficient in ORDER_STAFF_SALARY_COEFFICIENT:
                if str(order_staff.staff.experience) == coefficient[0]:
                    num_coff = staff_part * coefficient[1] / base_num
                    num_coefficient.append([order_staff.staff, num_coff])
        return num_coefficient

    def manager_report_salary_staffs(self):
        staff_list = self.order_cleaners.all()
        staff_salary = []
        if staff_list.filter(is_accept=True):
            num_coefficient = self.manager_report_numeric_coefficient(staff_list.filter(is_accept=True))
            [staff_salary.append([nc[0], int(self.cleaners_part) * nc[1]]) for nc in
             num_coefficient]
        if staff_list.filter(is_refuse=True):
            [staff_salary.append([staff_is_refuse.staff, None]) for staff_is_refuse in
             staff_list.filter(is_refuse=True)]
        return staff_salary

    def get_total(self):
        total = 0
        if self.status != 'canceled':
            services = self.order_services.filter(order=self)
            for service in services:
                total += service.service_total()
            if total > 2000:
                return total
            else:
                return 2000
        else:
            return 0

    #
    # def save(self, *args, **kwargs):
    #     self.work_end = self.work_start + self.cleaning_time
    #     super(Order, self).save(*args, **kwargs)

    class Meta:
        db_table = 'order'
        verbose_name = _('Заказ')
        verbose_name_plural = _('Заказы')
        permissions = [
            ('сan_view_income_outcome_report', 'Может просмотреть отчет о расходах и доходах'),
            ('can_view_order_deleted_list', 'Может просмотреть список удаленных заказов')
        ]


class Fine(models.Model):
    category = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Категория'))
    fine = models.CharField(max_length=300, null=True, blank=True, verbose_name=_('Штраф'))
    criteria = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Критерий'))
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Сумма штрафа'))
    description = models.TextField(max_length=500, blank=True, null=True, verbose_name=_('Пояснение'))

    def __str__(self):
        return f"{self.fine}"

    def get_absolute_url(self):
        return reverse('crmapp:fine_list')

    class Meta:
        db_table = 'fine'
        verbose_name = _('Штраф')
        verbose_name_plural = _('Штрафы')


class Bonus(models.Model):
    bonus = models.CharField(max_length=300, null=False, blank=False, verbose_name=_('Бонус'))
    value = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name=_('Сумма бонуса'))

    def __str__(self):
        return f"{self.bonus}"

    def get_absolute_url(self):
        return reverse('crmapp:bonus_list')

    class Meta:
        db_table = 'bonus'
        verbose_name = _('Бонус')
        verbose_name_plural = _('Бонусы')


class Inventory(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Инвентарь'), null=False, blank=False)
    description = models.TextField(max_length=1000, verbose_name=_('Описание'), null=True, blank=True)

    def get_absolute_url(self):
        return reverse('crmapp:inventory_index')

    def __str__(self):
        return f"{self.name}"

    class Meta:
        db_table = "inventory"
        verbose_name = _("Инвентарь")
        verbose_name_plural = _("Инвентари")


class ServiceOrder(models.Model):
    order = models.ForeignKey('crmapp.Order', related_name='order_services', verbose_name=_('Заказ'), null=True,
                              blank=True, on_delete=models.PROTECT)
    service = models.ForeignKey('crmapp.Service', related_name='service_orders', verbose_name=_('Услуга'),
                                null=False, blank=False, on_delete=models.PROTECT)
    amount = models.IntegerField(verbose_name=_('Объем работы'), null=False, blank=False,
                                 validators=[MinValueValidator(1)])
    rate = models.DecimalField(default=1, null=False, blank=False, verbose_name=_('Коэффицент сложности'),
                               max_digits=2, decimal_places=1,
                               validators=[MinValueValidator(1.0), MaxValueValidator(3.0)])
    total = models.PositiveIntegerField(null=True, blank=True, verbose_name=_('Стоимость услуги'))

    def __str__(self):
        return f"{self.service}: {self.service_total()} сом"

    def service_total(self):
        return self.service.price * self.amount * self.rate

    def get_total(self):
        total = 0
        for i in self.service_total():
            total += i
        return total

    class Meta:
        db_table = "service_order"
        verbose_name = _("Услуга заказа")
        verbose_name_plural = _("Услуги заказа")


class InventoryOrder(models.Model):
    order = models.ForeignKey('crmapp.Order', related_name='order_inventories', verbose_name=_('Заказ'),
                              null=True, blank=True, on_delete=models.PROTECT)
    inventory = models.ForeignKey('crmapp.Inventory', related_name='inventories_order',
                                  verbose_name=_('Инвентарь'), null=True, blank=True, on_delete=models.PROTECT)
    amount = models.PositiveIntegerField(verbose_name=_('Количество'), null=False, blank=False, default='1',
                                         validators=[MinValueValidator(1)])

    def get_absolute_url(self):
        return reverse('crmapp:inventory_index', pk=self.order.pk)

    def __str__(self):
        return f'{self.inventory}:{self.amount}'

    class Meta:
        db_table = 'inventory_in_order'
        verbose_name = _('Инвентарь заказа')
        verbose_name_plural = _('Инвентари заказа')


class ManagerReport(models.Model):
    order = models.ForeignKey('crmapp.Order', related_name='order_manager', on_delete=models.PROTECT,
                              verbose_name=_('Заказ'))
    cleaner = models.ForeignKey(get_user_model(), related_name='manager_report', on_delete=models.PROTECT,
                                verbose_name=_('Клинер'))
    salary = models.IntegerField(verbose_name=_('Заработная плата'), null=False, blank=False)
    fine = models.IntegerField(verbose_name=_('Штраф'), null=True, blank=True, default=0)
    fine_description = models.ForeignKey('crmapp.Fine', related_name='manager_reports', on_delete=models.PROTECT,
                                         null=True, blank=True, verbose_name=_('Причина штрафа'))
    bonus = models.IntegerField(verbose_name=_('Бонус'), null=True, blank=True, default=0)
    bonus_description = models.ForeignKey('crmapp.Bonus', related_name='manager_reports', on_delete=models.PROTECT,
                                          null=True, blank=True, verbose_name=_('Причина для бонуса'))
    created_at = models.DateTimeField(auto_now=True, verbose_name=_('Дата создания'))
    comment = models.CharField(max_length=255, null=True, blank=True, verbose_name=_('Комментарий'))

    def get_salary(self):
        total = self.salary + abs(self.bonus) - abs(self.fine)
        return total

    class Meta:
        db_table = 'manager_report'
        verbose_name = _('Отчет менеджера')
        verbose_name_plural = _('Отчеты менеджера')


class ObjectType(models.Model):
    name = models.CharField(max_length=255, verbose_name=_('Наименование'), null=False, blank=False)

    def __str__(self):
        return f'{self.name}'

    def get_absolute_url(self):
        return reverse('crmapp:object_type_list')

    class Meta:
        db_table = 'object_types'
        verbose_name = _('Тип объекта')
        verbose_name_plural = _('Типы объекта')


class CashManager(models.Model):
    staff = models.ForeignKey(get_user_model(), null=False, blank=False, related_name='manager_cash',
                              verbose_name=_('Менеджер'), on_delete=models.PROTECT)
    order = models.ForeignKey('crmapp.Order', related_name='order_manager_cash', verbose_name=_('Заказ'), null=False,
                              blank=False, on_delete=models.PROTECT)
    date = models.DateTimeField(auto_now_add=True, verbose_name=_("Дата создание"))
    is_nullify = models.BooleanField(default=False)

    def set_nullify_true(self):
        self.is_nullify = True
        self.save()

    def __str__(self):
        return f"{self.staff} - {self.order} -- {self.is_nullify}"

    class Meta:
        db_table = 'payout_cash_manager'
        verbose_name = _('Касса менеджера')
        verbose_name_plural = _('Касса менеджеров')
