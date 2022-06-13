from django.contrib import admin

from crmapp.models import Service, Client, Inventory, Fine, Bonus, \
    FineCategory, Order, ForemanOrderUpdate, ServiceOrder, StaffOrder, \
    InventoryOrder, ManagerReport, ObjectType


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


admin.site.register(Service)
admin.site.register(Client)
admin.site.register(Fine)
admin.site.register(FineCategory)
admin.site.register(Bonus)
admin.site.register(Inventory)
admin.site.register(Order, OrderAdmin)
admin.site.register(ForemanOrderUpdate)
admin.site.register(ServiceOrder, )
admin.site.register(InventoryOrder)
admin.site.register(ManagerReport)
admin.site.register(ObjectType)

