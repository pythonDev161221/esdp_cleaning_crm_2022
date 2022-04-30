from django import forms
from django.contrib.auth import get_user_model
from django.forms import BaseModelFormSet

from crmapp.models import Inventory, Cleanser, Client, ForemanOrderUpdate, ServiceOrder, \
    Service, ManagerReport, StaffOrder


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


class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ("service", "amount", "rate")


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


class BaseStaffAddFormSet(BaseModelFormSet):
    def init(self, *args, **kwargs):
        super().init(*args, **kwargs)