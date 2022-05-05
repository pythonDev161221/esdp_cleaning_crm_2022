from django.db.models import TextChoices
from django.utils.translation import gettext as _

MONDAY = 0
TUESDAY = 1
WEDNESDAY = 2
THURSDAY = 3
FRIDAY = 4
SATURDAY = 5
SUNDAY = 6


class WorkDayChoices(TextChoices):
    MONDAY = 'monday', _('Понедельник')
    TUESDAY = 'tuesday', _('Вторник')
    WEDNESDAY = 'wednesday', _('Среда')
    THURSDAY = 'thursday', _('Четверг')
    FRIDAY = 'friday', _('Пятница')
    SATURDAY = 'saturday', _('Суббота')
    SUNDAY = 'sunday', _('Воскресенье')


class StaffCategoryChoices(TextChoices):
    TRAINEE = 'trainee', _('Стажер')
    SKILLED = 'skilled', _('Опытный')
    EXPERT = 'expert', _('Профессионал')