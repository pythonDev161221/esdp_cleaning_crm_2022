from django.contrib import admin

# Register your models here.
from crmapp.models import TypeOfCleaning, TypeOfObjectAndClean, TypeOfObject

admin.site.register(TypeOfCleaning)
admin.site.register(TypeOfObjectAndClean)
admin.site.register(TypeOfObject)
