import calendar
from datetime import datetime
from django.utils.translation import gettext as _
from django.contrib.auth import get_user_model
from telegram import Update
from telegram.ext import CallbackContext
from crmapp.models import StaffOrder, ManagerReport, Order

User = get_user_model()


def get_finished_orders(update: Update, context: CallbackContext):
    all_orders = []
    chat_id = update.message.chat_id
    user = User.objects.get(telegram_id=chat_id)
    order = Order.objects.all().filter(cleaners=user).filter(status='finished')
    if order:
        for item in order:
            manager = ManagerReport.objects.get(order=item, cleaner=user)
            order_info = f'''
Заказ № {item.id}
Адрес: {item.address}
Дата: {_(calendar.day_name[item.work_start.isoweekday()])}, {item.work_start.date()}
Cумма: {manager.get_salary()} coм
'''
            all_orders.append(order_info)
        orders = '\n'.join(map(str, all_orders))
        text = f'Ваши завершенные заказы,cэр!\n{orders}'
    else:
        text = 'Ой,вы еще ничего не сделали...'
    context.bot.send_message(chat_id, text=text)


def get_new_orders(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user = User.objects.get(telegram_id=chat_id)
    order = Order.objects.all().filter(cleaners=user).filter(status='new').filter(
        work_start__date__gt=datetime.now().date())
    new_orders = []
    if order:
        for item in order:
            order_info = f'''
Заказ № {item.id}
Адрес: {item.address}
Дата: {item.work_start.date()}, {_(calendar.day_name[item.work_start.weekday()])}
Время: {item.work_start.astimezone().time()}
'''
            new_orders.append(order_info)
        orders = '\n'.join(map(str, new_orders))
        text = f'Вас ждут на этих заказах,cэр!\n{orders}'
    else:
        text = 'Заказов нет'
    context.bot.send_message(chat_id, text=text)


def get_today_orders(update: Update, context: CallbackContext):
    today_orders = []
    chat_id = update.message.chat_id
    user = User.objects.get(telegram_id=chat_id)
    order = Order.objects.all().filter(cleaners=user).filter(work_start__date=datetime.now().date())
    if order:
        for item in order:
            order_info = f'''
    Заказ № {item.id}
    Адрес: {item.address}
    Дата: {item.work_start.date()}, {_(calendar.day_name[item.work_start.weekday()])}
    Время: {item.work_start.astimezone().time()}
    Статус: {item.get_status_display()}
    '''
            if item.status == 'Завершен':
                staff_list = StaffOrder.objects.get(order=item, staff=user)
                manager_report = ManagerReport.objects.get(order=item, cleaner=staff_list.staff)
                order_info.join(f"Ваш баланс: {manager_report.get_salary()}")
                print(manager_report.get_salary())
            today_orders.append(order_info)
        orders = '\n'.join(map(str, today_orders))
        text = f'Ваши заказы на сегодня!{orders}'
    else:
        text = 'Заказов нет'
    context.bot.send_message(chat_id, text=text)
