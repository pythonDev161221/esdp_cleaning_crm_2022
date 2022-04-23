from django import forms

from crmapp.models import Inventory, Cleansear, Client, ForemanOrderUpdate, ServiceOrder, ExtraServiceOrder, ExtraService, ServiceOrder
class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'phone')

class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('name', 'amount')

class CleansearForm(forms.ModelForm):
    class Meta:
        model = Cleansear
        fields = ('name', 'description', 'unit', 'price', 'amount')

class ForemanOrderUpdateForm(forms.ModelForm):
    class Meta:
        model = ForemanOrderUpdate
        fields = ('description', )

class ForemanService(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ('service', 'amount', 'rate', 'total')

class ForemanExtraService(forms.ModelForm):
    class Meta:
        model = ExtraServiceOrder
        fields = ('extra_service', 'amount', 'rate', 'total')


class ExtraServiceForm(forms.ModelForm):
    class Meta:
        model = ExtraService
        fields = ("name", "unit", "price", "cleaning_time")

class ExtraServiceForm(forms.ModelForm):
    class Meta:
        model = ExtraService
        fields = ("name", "unit", "price", "cleaning_time")


class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ("service", "amount", "rate")

