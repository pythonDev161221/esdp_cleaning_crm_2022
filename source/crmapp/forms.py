from django import forms
from django.core.exceptions import ValidationError

from django.forms import modelformset_factory

from django.contrib.auth import get_user_model
from django.forms import BaseModelFormSet

from crmapp.models import Inventory, Client, ServiceOrder, \
    Service, ManagerReport, StaffOrder, Order, InventoryOrder, ForemanExpenses, ObjectType, Fine, Bonus, CashManager

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
            'client_info',
            'address',
            'work_start',
            'object_type',
            'payment_type',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields:
            if field == 'work_start':
                self.fields[field].widget = forms.DateInput(
                    attrs={
                        "type": 'datetime-local',
                        'required': True,
                        'class': 'date-time-picker form-control input-default',
                        'data-options': '{'
                                        '"format":"Y-m-d H:i", '
                                        '"timepicker":"true"'
                                        '}'
                    }
                )
            else:
                self.fields[field].widget.attrs.update({'class': 'form-control input-default'})


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

    def __init__(self, *args, **kwargs):
        super(ServiceOrderForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['min'] = 1
        self.fields['rate'].widget.attrs['max'] = 3

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

    def __init__(self, *args, **kwargs):
        super(InventoryOrderForm, self).__init__(*args, **kwargs)
        self.fields['amount'].widget.attrs['min'] = 1


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


class ManagerCashForm(forms.ModelForm):
    class Meta:
        model = CashManager
        fields = ['staff', ]


class ObjectTypeForm(forms.ModelForm):
    class Meta:
        model = ObjectType
        fields = ('name',)


class FineForm(forms.ModelForm):
    class Meta:
        model = Fine
        fields = ('category', 'fine', 'criteria', 'value', 'description')


class BonusForm(forms.ModelForm):
    class Meta:
        model = Bonus
        fields = ('bonus', 'value')
