from django.db.models import TextChoices
from django.utils.translation import gettext as _


class PaymentChoices(TextChoices):
    CASH = 'cash', _('Наличная оплата')
    VISA = 'visa', _('Безналичная оплата')


class UnitChoices(TextChoices):
    SQUARE_METER = 'square_meter', _('м²')
    PIECE = 'piece', _('шт.')
    SEAT_PLACE = 'seat_place', _('посад/место')
    SASH = 'sash', _('створка')
