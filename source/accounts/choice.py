from django.db.models import TextChoices
from django.utils.translation import gettext as _


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