from django import forms

from crmapp.models import Inventory, Cleansear, Client


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

