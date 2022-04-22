from django import forms

from crmapp.models import ExtraService, ServiceOrder


class ExtraServiceForm(forms.ModelForm):
    class Meta:
        model = ExtraService
        fields = ("name", "unit", "price", "cleaning_time")


class ServiceOrderForm(forms.ModelForm):
    class Meta:
        model = ServiceOrder
        fields = ("service", "amount", "rate")

