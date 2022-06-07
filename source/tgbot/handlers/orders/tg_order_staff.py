from tgbot.dispatcher import bot
from tgbot.handlers.keyboard import get_staff_order_keyboard

from crmapp.models import StaffOrder


def staff_accept_order(order):
    text = f'''
Информация о заказе №{order.pk}
 ◉ Дата: {order.work_start.date()}
 ◉ Время: {order.work_start.time()}
 ◉ Адрес: {order.address}
'''
    for staff in order.order_cleaners.all():
        if not staff.is_accept == True or staff.is_refuse == True:
            keyboard = get_staff_order_keyboard(order.pk, staff.staff.pk)
            bot.send_message(chat_id=staff.staff.telegram_id, text=text, reply_markup=keyboard)


def once_staff_add_order(staff: StaffOrder):
    text = f'''
Информация о заказе №{staff.order.pk}
 ◉ Дата: {staff.order.work_start.date()}
 ◉ Время: {staff.order.work_start.time()}
 ◉ Адрес: {staff.order.address}
    '''
    if not staff.is_accept == True or staff.is_refuse == True:
        keyboard = get_staff_order_keyboard(staff.order.pk, staff.staff.pk)
        bot.send_message(chat_id=staff.staff.telegram_id, text=text, reply_markup=keyboard)


def once_staff_remove_order(staff: StaffOrder):
    text = f"Вы были удалены с заказа №{staff.order.pk}"
    bot.send_message(chat_id=staff.staff.telegram_id, text=text)
