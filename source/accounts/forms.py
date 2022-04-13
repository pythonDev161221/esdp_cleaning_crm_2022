from django import forms
from django.contrib.auth.forms import UserCreationForm

from accounts.models import Staff


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        fields = ("username", "password1", "password2", "email", "first_name", "last_name")

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ("full_name", "inn_passport", "num_passport", "phone", "email", "avatar", "schedule")
