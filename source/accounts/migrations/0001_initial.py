# Generated by Django 4.0.4 on 2022-05-29 06:39

from django.conf import settings
import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Staff',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('email', models.EmailField(max_length=254, unique=True, verbose_name='Адрес электронной почты')),
                ('inn_passport', models.CharField(blank=True, max_length=20, null=True, unique=True, verbose_name='ИНН')),
                ('passport', models.FileField(blank=True, null=True, upload_to='passport/', verbose_name='Электронная версия паспорта')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=15, region='KG', verbose_name='Номер телефона')),
                ('avatar', models.ImageField(blank=True, null=True, upload_to='avatars/', verbose_name='Фото профиля')),
                ('address', models.CharField(blank=True, max_length=200, null=True, verbose_name='Адрес')),
                ('online_wallet', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(blank=True, max_length=256, null=True), blank=True, null=True, size=4, verbose_name='Электронные кошельки')),
                ('experience', models.CharField(choices=[('trainee', 'Стажер'), ('skilled', 'Опытный'), ('expert', 'Профессионал')], default='trainee', max_length=25, verbose_name='Опыт работы')),
                ('black_list', models.BooleanField(default=False, verbose_name='Черный список')),
                ('balance', models.IntegerField(default=0, verbose_name='Деньги работника')),
                ('description', models.TextField(blank=True, max_length=2000, null=True, verbose_name='Примечание')),
                ('telegram_id', models.CharField(blank=True, max_length=120, null=True)),
                ('telegram_auth_token', models.CharField(blank=True, max_length=21, null=True)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
            ],
            options={
                'verbose_name': 'Сотрудник',
                'verbose_name_plural': 'Сотрудники',
                'db_table': 'staff',
            },
        ),
        migrations.CreateModel(
            name='WorkDay',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day', models.CharField(choices=[('monday', 'Понедельник'), ('tuesday', 'Вторник'), ('wednesday', 'Среда'), ('thursday', 'Четверг'), ('friday', 'Пятница'), ('saturday', 'Суббота'), ('sunday', 'Воскресенье')], default='monday', max_length=25, verbose_name='День недели')),
            ],
            options={
                'verbose_name': 'День недели',
                'verbose_name_plural': 'Дни недели',
                'db_table': 'work_days',
            },
        ),
        migrations.CreateModel(
            name='Payout',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('salary', models.IntegerField(verbose_name='Заработная плата')),
                ('date_payout', models.DateTimeField(auto_now=True)),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='payouts', to=settings.AUTH_USER_MODEL, verbose_name='Работник')),
            ],
            options={
                'verbose_name': 'Выплата',
                'verbose_name_plural': 'Выплаты',
                'db_table': 'payout',
            },
        ),
        migrations.AddField(
            model_name='staff',
            name='schedule',
            field=models.ManyToManyField(default='monday', related_name='workday', to='accounts.workday', verbose_name='График работы'),
        ),
        migrations.AddField(
            model_name='staff',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions'),
        ),
    ]
