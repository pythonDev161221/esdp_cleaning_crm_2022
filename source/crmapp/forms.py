from django import forms

from crmapp.models import ExtraService


class ExtraServiceForm(forms.ModelForm):
    class Meta:
        model = ExtraService
        fields = ("name", "unit", "price", "cleaning_time")