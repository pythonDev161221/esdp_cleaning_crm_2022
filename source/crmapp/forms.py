from django import forms
from django.core.exceptions import ValidationError

from django.forms import inlineformset_factory, modelformset_factory

from django.contrib.auth import get_user_model
from django.forms import BaseModelFormSet

from crmapp.models import Inventory, Client, ForemanOrderUpdate, ServiceOrder, \
    Service, ManagerReport, StaffOrder, Order, InventoryOrder, ForemanExpenses

User = get_user_model()


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'unit', 'price', 'is_extra')


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'phone', 'organization')


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('name', 'description')


class ForemanExpenseForm(forms.ModelForm):
    class Meta:
        model = ForemanExpenses
        exclude = ('foreman_report',)

    def clean(self):
        cleaned_data = super().clean()
        if cleaned_data['amount'] <= 0:
            raise ValidationError('Расход не может быть 0!')
        else:
            return cleaned_data


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'object_type',
            'payment_type',
            'work_start',
            'cleaning_time',
            'client_info',
            'address',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['work_start'].widget = forms.DateInput(
            attrs={
                "type": 'datetime-local',
                'required': True,
                'class': 'date-time-picker',
                'data-options': '{'
                                '"format":"Y-m-d H:i", '
                                '"timepicker":"true"'
                                '}'
            }
        )
        self.fields["cleaning_time"].widget = forms.TimeInput(attrs={"placeholder": "ЧЧ:ММ:СС", "value": "00:00:00"})


class CleanersPartForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = (
            'part_units',
            'cleaners_part',
        )

    def is_percent(self):
        return True if self.cleaned_data.get('part_units') == 'percent' else False

    def get_cleaners_part(self):
        return self.cleaned_data.get('cleaners_part')

    def save(self, commit=True):
        order = super().save(commit=False)
        cleaners_part = self.get_cleaners_part()
        if self.is_percent():
            cleaners_part = int(order.get_total()) * (cleaners_part / 100)
        self.instance.cleaners_part = cleaners_part
        if commit:
            order.save()
        return order

    def clean_cleaners_part(self):
        cleaners_part = self.get_cleaners_part()
        if self.is_percent() and cleaners_part > 50:
            raise forms.ValidationError('Доля клинеров не может быть больше 50%')
        return cleaners_part


class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        exclude = (
            'order',
            'foreman_order',
            'total'
        )

    def save(self, commit=True):
        service = super().save(commit=False)
        self.instance.total = service.service_total()
        if commit:
            service.save()
        return service

    def clean_rate(self):
        rate = float(self.cleaned_data.get('rate'))
        if 3 < rate or rate < 1:
            raise forms.ValidationError('Введите диапазон от 1 до 3')
        return rate


class ManagerReportForm(forms.ModelForm):
    class Meta:
        model = ManagerReport
        fields = ('cleaner', 'salary', 'fine', 'fine_description', 'bonus', 'bonus_description', 'comment')


class BaseManagerReportFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = User.objects.none()


class OrderStaffForm(forms.ModelForm):
    class Meta:
        model = StaffOrder
        fields = ("staff", "is_brigadier")


class BaseStaffAddFormSet(BaseModelFormSet):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.queryset = User.objects.none()


class InventoryOrderForm(forms.ModelForm):
    class Meta:
        model = InventoryOrder
        exclude = ('order',)


InventoryOrderFormSet = modelformset_factory(InventoryOrder, form=InventoryOrderForm,
                                             exclude=['order'], extra=3, can_delete=False)


class FilterForm(forms.Form):
    start_date = forms.DateField(required=False)
    end_date = forms.DateField(required=False)


class SearchForm(forms.Form):
    search = forms.CharField(max_length=30, required=False, label="Найти")


class OrderCommentForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['description', ]