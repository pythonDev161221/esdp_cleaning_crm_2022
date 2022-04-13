from django.contrib import admin


from crmapp.models import ExtraService, TypeOfCleaning, TypeOfObjectAndClean, TypeOfObject, ComplexityFactor


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
admin.site.register(TypeOfCleaning)
admin.site.register(TypeOfObjectAndClean)
admin.site.register(TypeOfObject)
