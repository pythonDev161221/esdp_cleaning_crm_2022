from django import forms
from django.contrib.auth.forms import UserCreationForm, UsernameField

from accounts.models import Staff, Payout

from crispy_forms.helper import FormHelper


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class StaffRegistrationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = Staff
        fields = (
            "email",
            "first_name",
            "last_name",
            "password1",
            "password2",
            "phone",
            "inn_passport",
            "passport",
            "address",
            "online_wallet",
            "experience",
            "schedule")
        field_classes = {'username': UsernameField}
        widgets = {
            'schedule': forms.CheckboxSelectMultiple,
        }

        def __init__(self, *args, **kwargs):
            super(StaffRegistrationForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = True

        def clean(self):
            cleaned_data = super().clean()
            schedule = cleaned_data.get('schedule')
            if not schedule:
                raise forms.ValidationError('Выберите хотя бы один день')

        def save(self, commit=True):
            user = super(UserCreationForm, self).save(commit=False)
            user.set_password(self.cleaned_data["password1"])
            if commit:
                user.save()
            return user


class StaffEditForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ("email",
                  "first_name",
                  "last_name",
                  "phone",
                  "address",
                  "online_wallet",
                  "experience",
                  "schedule")
        widgets = {
            'schedule': forms.CheckboxSelectMultiple,
        }

        def __init__(self, *args, **kwargs):
            super(StaffEditForm, self).__init__(*args, **kwargs)
            self.helper = FormHelper()
            self.helper.form_tag = True

        def clean(self):
            cleaned_data = super().clean()
            schedule = cleaned_data.get('schedule')
            if not schedule:
                raise forms.ValidationError('Выберите хотя бы один день')


class EditPhotoForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["avatar", ]


class StaffPassportForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["passport", ]


class StaffDescriptionForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["description", ]

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['description'].widget.attrs.update(
            {
                'class': 'form-control',
                'placeholder': 'Введите примечание',
                'cols': 30,
                'rows': 2
            }
        )


class PasswordChangeForm(forms.ModelForm):
    password = forms.CharField(label="Новый пароль", strip=False, widget=forms.PasswordInput)
    password_confirm = forms.CharField(label="Подтвердите пароль", strip=False, widget=forms.PasswordInput)
    old_password = forms.CharField(label="Старый пароль", strip=False, widget=forms.PasswordInput)

    def clean_password_confirm(self):
        password = self.cleaned_data.get("password")
        password_confirm = self.cleaned_data.get("password_confirm")
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Пароли не совпадают!')
        return password_confirm

    def clean_old_password(self):
        old_password = self.cleaned_data.get('old_password')
        if not self.instance.check_password(old_password):
            raise forms.ValidationError('Старый пароль неправильный!')
        return old_password

    def save(self, commit=True):
        user = self.instance
        user.set_password(self.cleaned_data["password"])
        if commit:
            user.save()

        return user

    class Meta:
        model = Staff
        fields = ['old_password', 'password', 'password_confirm']


class PayoutForm(forms.ModelForm):
    class Meta:
        model = Payout
        fields = ['staff', ]

