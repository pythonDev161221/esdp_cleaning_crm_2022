from django.contrib import admin


from crmapp.models import ExtraService, CleaningSort, Service, PropertySort, ComplexityFactor, Client

from source.crmapp.models import Inventory, Cleansear


class ExtraServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    fields = ['name', 'unit', 'price', 'cleaning_time']


class ComplexityFactorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    fields = ['name', 'factor', 'description']

admin.site.register(ExtraService, ExtraServiceAdmin)
admin.site.register(ComplexityFactor, ComplexityFactorAdmin)
admin.site.register(CleaningSort)
admin.site.register(Service)
admin.site.register(PropertySort)
admin.site.register(Client)
admin.site.register(Inventory)
admin.site.register(Cleansear)
