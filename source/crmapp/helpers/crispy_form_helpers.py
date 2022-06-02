from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Row, Column


class BaseHelper(FormHelper):
    form_tag = False
    label_class = 'text-black-50'


class ServiceFormHelper(BaseHelper):
    disable_csrf = True
    layout = Layout(
        Row(
            Column('service', css_class='form-group col-md-6 mb-0'),
            Column('amount', css_class='form-group col-md-3 mb-0'),
            Column('rate', css_class='form-group col-md-3 mb-0'),
            css_class='form-row'
        )
    )


class OrderFormHelper(BaseHelper):
    layout = Layout(
        Row(
            Column('object_type', css_class='form-group col-md-3 mb-0'),
            Column('payment_type', css_class='form-group col-md-3 mb-0'),
            Column('work_start', css_class='form-group col-md-3 mb-0'),
            Column('cleaning_time', css_class='form-group col-md-3 mb-0'),
            css_class='form-row'
        ),
        Row(
            Column('client_info', css_class='form-group col-md-6 mb-0'),
            Column('address', css_class='form-group col-md-6 mb-0'),
            css_class='form-row'
        )
    )


class CleanersPartHelper(BaseHelper):
    layout = Layout(
        Row(
            Column('cleaners_part', css_class='form-group col-md-3 mb-0'),
            Column('part_units', css_class='form-group col-md-3 mb-0'),
            css_class='form-row'
        ),
    )


class StaffFormHelper(BaseHelper):
    disable_csrf = True
    layout = Layout(
        Row(
            Column('staff', css_class='form-group col-md-3 mb-0'),
            Column('is_brigadier', css_class='form-group col-md-3 mb-0'),
            css_class='form-row'
        )
    )
