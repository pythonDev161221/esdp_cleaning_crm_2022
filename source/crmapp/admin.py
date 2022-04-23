from django.contrib import admin


from crmapp.models import ExtraService, CleaningSort, Service, PropertySort, \
    ComplexityFactor, Client, Inventory, Cleansear, Fine, Bonus, \
    FineCategory, Order, ForemanReport, ForemanOrderUpdate, ExtraServiceOrder, ServiceOrder, Foreman, Cleaners


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
admin.site.register(Fine)
admin.site.register(FineCategory)
admin.site.register(Bonus)
admin.site.register(Inventory)
admin.site.register(Cleansear)
admin.site.register(Order)
admin.site.register(ForemanReport)
admin.site.register(ForemanOrderUpdate)
admin.site.register(ServiceOrder)
admin.site.register(ExtraServiceOrder)
admin.site.register(Foreman)
admin.site.register(Cleaners)

