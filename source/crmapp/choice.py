from django.db.models import TextChoices
from django.utils.translation import gettext as _


class PaymentChoices(TextChoices):
    CASH = 'cash', _('Наличная оплата')
    VISA = 'visa', _('Безналичная оплата')


class PartUnits(TextChoices):
    SOM = 'som', _('В сомах')
    PERCENT = 'percent', _('В процентах')


class UnitChoices(TextChoices):
    SQUARE_METER = 'square_meter', _('м²')
    PIECE = 'piece', _('шт.')
    SEAT_PLACE = 'seat_place', _('посад/место')
    SASH = 'sash', _('створка')


class OrderStatusChoices(TextChoices):
    NEW = 'new', _('Новый')
    IN_QUEUE = 'in_queue', _('В очереди')
    IN_PROGRES = 'in_progres', _('Выполняется')
    DONE = 'done', _('Выполнен')
    DISPUTABLE = 'disputable', _('Спорный')
    TO_FIX = 'to_fix', _('Переделывается')
    FINISHED = 'finished', _('Завершен')
