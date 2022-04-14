from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _

class Staff(AbstractUser):
    inn_passport = models.CharField(max_length=20, null=False, blank=False, verbose_name=_('ИНН'))
    num_passport = models.CharField(max_length=20, null=False, blank=False, verbose_name=_('Номер паспорта'))
    phone = models.CharField(max_length=20, null=False, blank=False, verbose_name=_('Номер телефона'))
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name=_('Фото профиля'))
    schedule = models.ManyToManyField('accounts.WorkDay', null=True, blank=True, verbose_name=_('График работы'))#Нужно переделать

    def __str__(self):
        return f'{self.first_name} --- {self.last_name} --- {self.phone}'

    class Meta:
        db_table = 'Staff'
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')


class WorkDay(models.Model):
    DAYS_OF_WEEK = (
        (0, _('Monday')),
        (1, _('Tuesday')),
        (2, _('Wednesday')),
        (3, _('Thursday')),
        (4, _('Friday')),
        (5, _('Saturday')),
        (6, _('Sunday')),
    )
    day_of_the_week = models.IntegerField(
        verbose_name=_('day of the week'),
        choices=DAYS_OF_WEEK
    )

    def __str__(self):
        return f"{self.day_of_the_week}"

    class Meta:
        db_table = 'workdays'
        verbose_name = _('Рабочий день')
        verbose_name_plural = _('Рабочие дни')