from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext as _


class Staff(AbstractUser):
    CATEGORY_CHOICES = [
        ('Trainee', 'Стажер'),
        ('Skilled', 'C опытом'),
        ('Expert', 'Профессионал'),
    ]

    inn_passport = models.CharField(max_length=20, unique=True, null=False, blank=False, verbose_name=_('ИНН'))
    phone = models.CharField(max_length=20, null=False, blank=False, verbose_name=_('Номер телефона'))
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name=_('Фото профиля'))
    schedule = models.ManyToManyField('accounts.WorkDay', null=True, blank=True, verbose_name=_('График работы'))
    experience = models.CharField(max_length=256, choices=CATEGORY_CHOICES, null=False, blank=False,
                                  default='Trainee', verbose_name=_('Опыт работы'))
    black_list = models.BooleanField(default=False, verbose_name=_('В черном списке'))

    def __str__(self):
        return f'{self.first_name} --- {self.last_name} --- {self.experience} --- {self.phone} '

    class Meta:
        db_table = 'Staff'
        verbose_name = _('Сотрудник')
        verbose_name_plural = _('Сотрудники')


class WorkDay(models.Model):
    DAYS_OF_WEEK = (
        (1, _('Monday')),
        (2, _('Tuesday')),
        (3, _('Wednesday')),
        (4, _('Thursday')),
        (5, _('Friday')),
        (6, _('Saturday')),
        (0, _('Sunday')),
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