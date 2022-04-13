from django.contrib import admin

# Register your models here.
from crmapp.models import ExtraService


class ExtraServiceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']
    list_display_links = ['id', 'name']
    fields = ['name', 'unit', 'price', 'cleaning_time']


admin.site.register(ExtraService, ExtraServiceAdmin)