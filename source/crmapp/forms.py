from django import forms

from django.forms import inlineformset_factory

from crmapp.custom_layout_object import Formset

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, Fieldset, Row, Column, Submit

from django.contrib.auth import get_user_model
from django.forms import BaseModelFormSet

from crmapp.models import Inventory, Cleanser, Client, ForemanOrderUpdate, ServiceOrder, \
    Service, ManagerReport, StaffOrder, Order


User = get_user_model()


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'unit', 'price', 'is_extra')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'phone')


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('name', 'description')


class CleanserForm(forms.ModelForm):
    class Meta:
        model = Cleanser
        fields = ('name', 'description')


class ForemanOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = ForemanOrderUpdate
        fields = ('description',)


class ForemanService(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ('service', 'amount', 'rate', 'total')


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        exclude = ('services', 'cleaners',)

    def __init__(self, *args, **kwargs):
        super(OrderForm, self).__init__(*args, **kwargs)
        self.fields["work_start"].widget = forms.DateTimeInput(attrs={"type": "datetime-local"})
        self.fields["cleaning_time"].widget = forms.TimeInput(attrs={"type": "time"})
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.layout = Layout(
            Field('manager'),
            Row(
                Column('status', css_class='form-group col-md-4 mb-0'),
                Column('object_type', css_class='form-group col-md-4 mb-0'),
                Column('payment_type', css_class='form-group col-md-4 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('work_start', css_class='form-group col-md-6 mb-0'),
                Column('cleaning_time', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Row(
                Column('client_info', css_class='form-group col-md-6 mb-0'),
                Column('address', css_class='form-group col-md-6 mb-0'),
                css_class='form-row'
            ),
            Fieldset('Добавление клинеров',
                     Formset('cliners'), css_class='row form-row'),
            Fieldset('Добавление услуг',
                     Formset('services'), css_class='row form-row'),
            Submit('submit', 'Создать')
        )


class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        exclude = ('order',)

    def __init__(self, *args, **kwargs):
        super(ServiceOrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.label_class = 'visually-hidden'


ServiceOrderFormSet = inlineformset_factory(Order, ServiceOrder, form=ServiceOrderForm,
                                            exclude=['order'], extra=3, can_delete=False)


class StaffOrderForm(forms.ModelForm):
    class Meta:
        model = StaffOrder
        exclude = ('order',)

    def __init__(self, *args, **kwargs):
        super(StaffOrderForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.label_class = 'visually-hidden'


class ManagerReportForm(forms.ModelForm):
    class Meta:
        model = ManagerReport
        fields = ('cleaner', 'salary', 'fine', 'bonus')


class BaseManagerReportFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = User.objects.none()


class OrderStaffForm(forms.ModelForm):
    class Meta:
        model = StaffOrder
        fields = ("staff", "is_brigadier")

    def __init__(self, *args, **kwargs):
        super(OrderStaffForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_tag = True
        self.helper.label_class = 'visually-hidden'


StaffOrderFormSet = inlineformset_factory(Order, StaffOrder, form=OrderStaffForm,
                                          exclude=['order'], extra=3, can_delete=False)


class BaseStaffAddFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = User.objects.none()

