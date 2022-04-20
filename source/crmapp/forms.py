from django import forms

from crmapp.models import Service


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('cleaning_sort', 'property_sort', 'unit', 'price')

