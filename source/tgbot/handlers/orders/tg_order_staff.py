from tgbot.dispatcher import bot

from tgbot.handlers.keyboard import get_staff_order_keyboard


def staff_accept_order(order):

    text = f'''
Информация о заказе
 ◉ Дата: {order.work_start.date()}
 ◉ Время: {order.work_start.time()}
 ◉ Адрес: {order.address}
'''
    for staff in order.order_cleaners.all():
        if not staff.is_accept == True or staff.is_refuse == True:
            keyboard = get_staff_order_keyboard(order.pk, staff.staff.pk)
            bot.send_message(staff.staff.telegram_id, text, reply_markup=keyboard)
