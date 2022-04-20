from django import forms

from crmapp.models import Service, PropertySort, CleaningSort


class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ('cleaning_sort', 'property_sort', 'unit', 'price')


class PropertySortForm(forms.ModelForm):
    class Meta:
        model = PropertySort
        fields = ('name',)


class CleaningSortForm(forms.ModelForm):
    class Meta:
        model = CleaningSort
        fields = ('name',)
