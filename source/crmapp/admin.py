from django.contrib import admin

from crmapp.models import CleaningSort, Service, PropertySort, \
    ComplexityFactor, Client, Inventory, Cleansear, Fine, Bonus, \
    FineCategory, Order, ForemanReport, ForemanOrderUpdate, ServiceOrder, StaffOrder


class StaffOrderInline(admin.StackedInline):
    model = StaffOrder
    extra = 1
    fields = ['order', 'staff', 'is_brigadier']


class ServiceOrderInline(admin.StackedInline):
    model = ServiceOrder
    extra = 1
    fields = ['order', 'service', 'amount', 'rate', 'total']


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        StaffOrderInline, ServiceOrderInline
    ]


class ComplexityFactorAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    fields = ['name', 'factor', 'description']


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
admin.site.register(Order, OrderAdmin, )
admin.site.register(ForemanReport)
admin.site.register(ForemanOrderUpdate)
admin.site.register(ServiceOrder, )
