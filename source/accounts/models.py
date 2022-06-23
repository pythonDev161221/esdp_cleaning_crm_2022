import uuid

from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models, transaction
from django.urls import reverse
from django.utils.translation import gettext as _
from phonenumber_field.modelfields import PhoneNumberField

from .managers import CustomUserManager
from .choice import StaffCategoryChoices, WorkDayChoices
from main.settings import TELEGRAM_BOT_USERNAME


class Staff(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name=_('Email'))
    inn_passport = models.CharField(max_length=20, unique=True, null=True, blank=True, verbose_name=_('ИНН'))
    passport = models.FileField(upload_to='passport/', null=True, blank=True,
                                 verbose_name=_('Электронная версия паспорта'))
    phone = PhoneNumberField(region="KG", max_length=15, verbose_name=_('Номер телефона'))
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name=_('Фото профиля'))
    address = models.CharField(max_length=200, null=True, blank=True, verbose_name=_('Адрес'))
    online_wallet = ArrayField(
        models.CharField(max_length=256, null=True, blank=True),
        size=4, null=True, blank=True, verbose_name=_('Электронные кошельки')
    )
    schedule = models.ManyToManyField('accounts.WorkDay', related_name='workday', default='monday',
                                      verbose_name=_('График работы'))
    experience = models.CharField(max_length=25, choices=StaffCategoryChoices.choices, default='trainee', null=False,
                                  blank=False,
                                  verbose_name=_('Опыт работы'))
    black_list = models.BooleanField(default=False, verbose_name=_('Черный список'))
    balance = models.IntegerField(verbose_name=_('Деньги работника'), default=0,
                                  null=False, blank=False)
    cash = models.IntegerField(verbose_name=_('Касса менеджера'), default=0,
                                  null=False, blank=False)
    description = models.TextField(max_length=2000, null=True, blank=True, verbose_name=_('Примечание'))
    telegram_id = models.CharField(max_length=120, null=True, blank=True)
    telegram_auth_token = models.CharField(max_length=21, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = CustomUserManager()

    def black_list_staff(self):
        self.black_list = True
        self.is_active = False
        self.save()

    def active_staff(self):
        self.black_list = False
        self.is_active = True
        self.save()

    def soft_delete(self):
        self.is_active = False
        self.save()

    def nullify_salary(self):
        self.balance = 0
        self.save()

    def nullify_cash(self):
        with transaction.atomic():
            self.manager_cash.all()
            [pay.set_nullify_true() for pay in self.manager_cash.all()]
            self.cash = 0
            self.save()

    def add_cash(self, value):
        self.cash += value
        self.save()

    def add_salary(self, value):
        self.balance += value
        self.save()

    def remove_salary(self, value):
        self.balance -= value
        self.save()

    def set_auth_tg_token(self):
        token = str(uuid.uuid4().hex)[:20]
        self.telegram_auth_token = token
        self.save()
        return f"https://t.me/{TELEGRAM_BOT_USERNAME}?start={token}"

    def __str__(self):
        return f' {self.last_name} {self.first_name}'

    def get_absolute_url(self):
        return reverse('accounts:profile', kwargs={'pk': self.pk})

    class Meta:
        db_table = 'staff'
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')
        permissions = (
            ('add_staff_passport_photo', 'добавить фото паспорта'),
            ('add_staff_description', 'добавить примечание'),
            ('view_staff_blacklist', 'просмотр черного листа'),
            ('add_toBlackList', 'добавить в черный список'),
            ('delete_fromBlackList', 'удалить из черного списка'),
        )


class WorkDay(models.Model):
    day = models.CharField(max_length=25, choices=WorkDayChoices.choices, default='monday', null=False,
                           blank=False, verbose_name=_('День недели'))

    def __str__(self):
        return self.get_day_display()

    class Meta:
        db_table = 'work_days'
        verbose_name = _('День недели')
        verbose_name_plural = _('Дни недели')


class Payout(models.Model):
    staff = models.ForeignKey('accounts.Staff', null=False, blank=False, related_name='payouts',
                              verbose_name=_('Работник'), on_delete=models.PROTECT)
    salary = models.IntegerField(null=False, blank=False,
                                 verbose_name=_('Сумма'))
    date_payout = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return reverse('accounts:payout_list')

    def __str__(self):
        return f"{self.date_payout}{self.staff}{self.salary}"

    class Meta:
        db_table = 'payout'
        verbose_name = _('Выплата')
        verbose_name_plural = _('Выплаты')
