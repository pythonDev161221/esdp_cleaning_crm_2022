from django import forms


from crmapp.models import Inventory, Cleansear, Client, ForemanOrderUpdate, ServiceOrder, ExtraServiceOrder, ExtraService, Service, PropertySort, CleaningSort


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


class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'phone')


class InventoryForm(forms.ModelForm):
    class Meta:
        model = Inventory
        fields = ('name', 'description')


class CleansearForm(forms.ModelForm):
    class Meta:
        model = Cleansear
        fields = ('name', 'description')


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

