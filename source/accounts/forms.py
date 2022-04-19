from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Staff
from crmapp.models import Client


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")


class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ("inn_passport", "phone", "email", "avatar", "schedule")

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'phone')
