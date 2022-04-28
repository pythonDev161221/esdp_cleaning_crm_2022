from django import forms
from crmapp.models import Inventory, Cleanser, Client, ForemanOrderUpdate, ServiceOrder, \
     Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('name', 'unit', 'price', 'cleaning_time', 'is_extra')


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
