from django.contrib.auth import get_user_model
from django.db import models

class Staff(models.Model):
    user = models.OneToOneField(get_user_model(), related_name="profile", verbose_name="Профиль", on_delete=models.CASCADE)
    full_name = models.CharField(max_length=100, null=False, blank=False, verbose_name='Ф.И.О.')
    inn_passport = models.CharField(max_length=20, null=False, blank=False, verbose_name='ИНН')
    num_passport = models.CharField(max_length=20, null=False, blank=False, verbose_name='Номер паспорта')
    phone = models.CharField(max_length=20, null=False, blank=False, verbose_name='Номер телефона')
    email = models.EmailField(null=False, blank=False, verbose_name='Электронная почта')
    avatar = models.ImageField(upload_to="avatars/", null=True, blank=True, verbose_name='Фото профиля')
    schedule = models.CharField(max_length=20, null=True, blank=True, verbose_name='График работы')#Нужно переделать