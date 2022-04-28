# Generated by Django 4.0.4 on 2022-04-28 04:08

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import phonenumber_field.modelfields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('accounts', '0002_alter_staff_email'),
    ]

    operations = [
        migrations.CreateModel(
            name='Bonus',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bonus', models.CharField(blank=True, max_length=300, null=True, verbose_name='Бонус')),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Сумма бонуса')),
            ],
            options={
                'verbose_name': 'Бонус',
                'verbose_name_plural': 'Бонусы',
                'db_table': 'bonus',
            },
        ),
        migrations.CreateModel(
            name='CleaningSort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200, verbose_name='Тип уборки')),
            ],
            options={
                'verbose_name': 'Тип уборки',
                'verbose_name_plural': 'Типы уборок',
                'db_table': 'cleaning_sort',
            },
        ),
        migrations.CreateModel(
            name='Cleanser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Моющее средство')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Описание товара')),
            ],
            options={
                'verbose_name': 'Моющее средство',
                'verbose_name_plural': 'Моющие средства',
                'db_table': 'cleanser',
            },
        ),
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('first_name', models.CharField(max_length=75, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=75, verbose_name='Фамилия')),
                ('phone', phonenumber_field.modelfields.PhoneNumberField(max_length=15, region='KG', unique=True, verbose_name='Номер телефона')),
            ],
            options={
                'verbose_name': 'Клиент',
                'verbose_name_plural': 'Клиенты',
                'db_table': 'client',
            },
        ),
        migrations.CreateModel(
            name='FineCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, null=True, verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Категория для штрафа',
                'verbose_name_plural': 'Категории для штрафа',
                'db_table': 'fine_category',
            },
        ),
        migrations.CreateModel(
            name='ForemanPhoto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='photo_obj', verbose_name='Фото')),
            ],
        ),
        migrations.CreateModel(
            name='Inventory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Инвентарь')),
                ('description', models.TextField(blank=True, max_length=1000, null=True, verbose_name='Описание')),
            ],
            options={
                'verbose_name': 'Инвентарь',
                'verbose_name_plural': 'Инвентари',
                'db_table': 'inventory',
            },
        ),
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_finished', models.BooleanField(default=False, verbose_name='Завершённая работа')),
                ('created_at', models.DateTimeField(auto_now_add=True, verbose_name='Дата и время создания заказа')),
                ('work_start', models.DateTimeField(verbose_name='Дата и время выполнения уборки')),
                ('work_time', models.TimeField(verbose_name='Время выполнения работ')),
                ('address', models.CharField(max_length=256, verbose_name='Адрес')),
                ('review', models.PositiveIntegerField(blank=True, null=True, validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)], verbose_name='Отзыв')),
                ('payment_type', models.CharField(choices=[('cash', 'Наличная оплата'), ('visa', 'Безналичная оплата')], default='cash', max_length=25, verbose_name='Вид оплаты')),
                ('total_cost', models.PositiveIntegerField(blank=True, null=True, verbose_name='Общая сумма заказа')),
            ],
        ),
        migrations.CreateModel(
            name='PropertySort',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, verbose_name='Тип объекта')),
            ],
            options={
                'verbose_name': 'Тип объекта',
                'verbose_name_plural': 'Типы объектов',
                'db_table': 'property_sort',
            },
        ),
        migrations.CreateModel(
            name='Service',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=300, verbose_name='Дополнительная услуга')),
                ('unit', models.CharField(choices=[('square_meter', 'м²'), ('piece', 'шт.')], max_length=350, verbose_name='Единица измерения')),
                ('price', models.PositiveIntegerField(verbose_name='Цена за единицу')),
                ('cleaning_time', models.IntegerField(blank=True, null=True, verbose_name='Расчетное время уборки')),
                ('is_extra', models.BooleanField(verbose_name='Доп. услуга')),
            ],
            options={
                'verbose_name': 'Услуга',
                'verbose_name_plural': 'Услуги',
                'db_table': 'services',
            },
        ),
        migrations.CreateModel(
            name='StaffOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_brigadier', models.BooleanField(default=False, verbose_name='Бригадир')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_cliners', to='crmapp.order', verbose_name='Заказ')),
                ('staff', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='cliner_orders', to=settings.AUTH_USER_MODEL, verbose_name='Клинер')),
            ],
        ),
        migrations.CreateModel(
            name='ServiceOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(verbose_name='Объем работы')),
                ('rate', models.DecimalField(decimal_places=1, default=1, max_digits=2, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(3.0)], verbose_name='Коэффицент сложности')),
                ('total', models.PositiveIntegerField(verbose_name='Стоимость услуги')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_services', to='crmapp.order', verbose_name='Заказ')),
                ('service', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='service_orders', to='crmapp.service', verbose_name='Услуга')),
            ],
            options={
                'verbose_name': 'Услуга заказа',
                'verbose_name_plural': 'Услуги заказа',
                'db_table': 'service_order',
            },
        ),
        migrations.AddField(
            model_name='order',
            name='cleaners',
            field=models.ManyToManyField(related_name='orders', through='crmapp.StaffOrder', to=settings.AUTH_USER_MODEL, verbose_name='Клинер'),
        ),
        migrations.AddField(
            model_name='order',
            name='client_info',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='order_client', to='crmapp.client', verbose_name='Информация клиента'),
        ),
        migrations.AddField(
            model_name='order',
            name='manager',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='manager_order', to=settings.AUTH_USER_MODEL, verbose_name='Менеджер'),
        ),
        migrations.AddField(
            model_name='order',
            name='services',
            field=models.ManyToManyField(related_name='orders', through='crmapp.ServiceOrder', to='crmapp.service', verbose_name='Услуга'),
        ),
        migrations.CreateModel(
            name='InventoryInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество')),
                ('inventory', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='inventories_order', to='crmapp.inventory', verbose_name='Инвентарь')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_inventories', to='crmapp.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Инвентарь заказа',
                'verbose_name_plural': 'Инвентари заказа',
                'db_table': 'inventory_in_order',
            },
        ),
        migrations.CreateModel(
            name='ForemanReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expenses', models.PositiveIntegerField(blank=True, null=True, verbose_name='Расходы')),
                ('start_at', models.DateTimeField(verbose_name='Дата и время начала работы')),
                ('end_at', models.DateTimeField(verbose_name='Дата и время окончания работы')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='foreman_order_report', to='crmapp.order', verbose_name='Заказ')),
                ('photo_after', models.ManyToManyField(related_name='foreman_photo_after', to='crmapp.foremanphoto', verbose_name='Фото после окончания работ')),
                ('photo_before', models.ManyToManyField(related_name='foreman_photo_before', to='crmapp.foremanphoto', verbose_name='Фото до начала работ')),
            ],
        ),
        migrations.CreateModel(
            name='ForemanOrderUpdate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Причина внесения изменений')),
                ('order', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='foreman_order_update', to='crmapp.order', verbose_name='Заказ')),
                ('service', models.ManyToManyField(related_name='foreman_service', to='crmapp.serviceorder', verbose_name='Услуга')),
            ],
        ),
        migrations.CreateModel(
            name='Fine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fine', models.CharField(blank=True, max_length=300, null=True, verbose_name='Штраф')),
                ('criteria', models.CharField(blank=True, max_length=255, null=True, verbose_name='Критерий')),
                ('value', models.DecimalField(blank=True, decimal_places=2, max_digits=10, null=True, verbose_name='Сумма штрафа')),
                ('description', models.TextField(blank=True, max_length=500, null=True, verbose_name='Пояснение')),
                ('category', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='fines', to='crmapp.finecategory', verbose_name='Категория')),
            ],
            options={
                'verbose_name': 'Штраф',
                'verbose_name_plural': 'Штрафы',
                'db_table': 'fine',
            },
        ),
        migrations.CreateModel(
            name='CleanserInOrder',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.PositiveIntegerField(blank=True, null=True, verbose_name='Количество')),
                ('cleanser', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='cleansers_order', to='crmapp.cleanser', verbose_name='Моющее средство')),
                ('order', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='order_cleanser', to='crmapp.order', verbose_name='Заказ')),
            ],
            options={
                'verbose_name': 'Моющее средство в заказе',
                'verbose_name_plural': 'Моющие средства в заказе',
                'db_table': 'cleanser_in_order',
            },
        ),
    ]
