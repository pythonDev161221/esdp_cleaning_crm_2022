from django.contrib import admin
from django.contrib.auth import get_user_model
from accounts.models import Staff, WorkDay, Payout

User = get_user_model()

admin.site.register(User)
admin.site.register(WorkDay)
admin.site.register(Payout)
