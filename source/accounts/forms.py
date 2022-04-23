from django import forms
from django.contrib.auth import password_validation
from django.contrib.auth.forms import UserCreationForm, UsernameField

from accounts.models import Staff


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)


class StaffRegistrationForm(UserCreationForm):
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')
    password1 = forms.CharField(
        label='Пароль',
        strip=False,
        widget=forms.PasswordInput(),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label='Повторите пароль',
        strip=False,
        widget=forms.PasswordInput(),
        help_text=password_validation.password_validators_help_text_html(),
    )
    inn_passport = forms.CharField(label='ИHH')
    phone = forms.CharField(label='Телефон')

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
            "address",
            "experience",
            "schedule")
        field_classes = {'username': UsernameField}
        widgets = {
            'schedule': forms.CheckboxSelectMultiple,
        }

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
    first_name = forms.CharField(label='Имя')
    last_name = forms.CharField(label='Фамилия')

    class Meta:
        model = Staff
        fields = ("email",
                  "first_name",
                  "last_name",
                  "phone",
                  "inn_passport",
                  "address",
                  "schedule")
        widgets = {
            'schedule': forms.CheckboxSelectMultiple,
        }

        def clean(self):
            cleaned_data = super().clean()
            schedule = cleaned_data.get('schedule')
            if not schedule:
                raise forms.ValidationError('Выберите хотя бы один день')


class EditPhotoForm(forms.ModelForm):
    class Meta:
        model = Staff
        fields = ["avatar", ]


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
