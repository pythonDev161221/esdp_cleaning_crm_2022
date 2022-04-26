from django.contrib import admin

from crmapp.models import ExtraService, CleaningSort, Service, PropertySort, \
    ComplexityFactor, Client, Inventory, Cleansear, Fine, Bonus, \
    FineCategory, Order, ForemanReport, ForemanOrderUpdate, ExtraServiceOrder, ServiceOrder, StaffOrder, \
    ServiceForemanOrderUpdate, ExtraServiceForemanOrderUpdate, ExtraServiceForemanOrderAdd, ServiceForemanOrderAdd


class ExtraServiceForemanOrderAddInline(admin.StackedInline):
    model = ExtraServiceForemanOrderAdd
    extra = 0
    fields = ['foreman_order_update', 'extra_service_added', 'amount', 'rate', 'total']


class ServiceForemanOrderAddInline(admin.StackedInline):
    model = ServiceForemanOrderAdd
    extra = 0
    fields = ['foreman_order_update', 'service_added', 'amount', 'rate', 'total']


class ServiceForemanOrderUpdateInline(admin.StackedInline):
    model = ServiceForemanOrderUpdate
    extra = 0
    fields = ['foreman_order_update', 'service_updated', 'amount', 'rate', 'total']


class ExtraServiceForemanOrderUpdateInline(admin.StackedInline):
    model = ExtraServiceForemanOrderUpdate
    extra = 0
    fields = ['foreman_order_update', 'extra_service_updated', 'amount', 'rate', 'total']


class ForemanOrderUpdateAdmin(admin.ModelAdmin):
    inlines = [
        ServiceForemanOrderUpdateInline, ExtraServiceForemanOrderUpdateInline, ServiceForemanOrderAddInline,
        ExtraServiceForemanOrderAddInline
    ]


class StaffOrderInline(admin.StackedInline):
    model = StaffOrder
    extra = 1
    fields = ['order', 'staff', 'is_brigadier']


class ServiceOrderInline(admin.StackedInline):
    model = ServiceOrder
    extra = 1
    fields = ['order', 'service', 'amount', 'rate', 'total']


class ExtraServiceOrderInline(admin.StackedInline):
    model = ExtraServiceOrder
    extra = 1
    fields = ['order', 'extra_service', 'amount', 'rate', 'total']


class OrderAdmin(admin.ModelAdmin):
    inlines = [
        StaffOrderInline, ServiceOrderInline, ExtraServiceOrderInline
    ]


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
admin.site.register(Order, OrderAdmin, )
admin.site.register(ForemanReport)
admin.site.register(ForemanOrderUpdate, ForemanOrderUpdateAdmin)
admin.site.register(ServiceOrder, )
admin.site.register(ExtraServiceOrder)
# admin.site.register(Foreman)
# admin.site.register(Cleaners)
