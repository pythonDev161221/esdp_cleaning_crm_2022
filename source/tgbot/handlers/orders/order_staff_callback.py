import datetime

from telegram import Update
from telegram.ext import CallbackContext
from crmapp.models import Order, ManagerReport
from django.db import transaction

from tgbot.handlers.keyboard import get_refuses_keyboard, get_staff_order_keyboard


def order_staff_accept_callback(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    order = Order.objects.get(pk=order_id)
    staff = order.order_cleaners.get(staff=staff_id)
    staff.is_accept = True
    staff.save()
    text = f'''
Информация о заказе
 ◉ Дата: {order.work_start.date()}
 ◉ Время: {order.work_start.time()}
 ◉ Адрес: {order.address}
Информация о клиенте
 ◉ Имя: {order.client_info.full_name}
 ◉ Телефон: {order.client_info.phone}
    '''
    print(datetime.datetime.now())
    context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)


def order_staff_refuse_callback(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    if call == "refuse":
        text = "Вы уверены что хотите отказаться от заказа?\nВ случае отказа вы получите штраф 200 сом"
        keyboard = get_refuses_keyboard(order_id, staff_id)
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboard)


def refuse_true_callback(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    order = Order.objects.get(pk=order_id)
    staff = order.order_cleaners.get(staff=staff_id)
    if call == "retrue":
        if staff.is_accept == False and staff.is_refuse == False:
            try:
                with transaction.atomic():
                    staff.is_refuse = True
                    fine_comment = "Отказ от заказа"
                    report = ManagerReport.objects.create(cleaner=staff.staff, order=order, fine=200, comment=fine_comment, salary=0)
                    staff.staff.remove_salary(abs(report.get_salary()))
                    staff.save()
                    text = f"Вы больше не участвуете в данном заказе №{order_id}"
                    context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)
            except:
                text = "Повроторите запрос пойзже"
                context.bot.send_message(chat_id, text)
        else:
            text = "Даный запрос не может быть выолнен"
            context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text)


def refuse_false_callback(update: Update, context: CallbackContext):
    chat_id = update.callback_query.message.chat.id
    message_id = update.callback_query.message.message_id
    data = update.callback_query.data
    call, order_id, staff_id = data.split(" ")
    order = Order.objects.get(pk=order_id)
    if call == "refalse":
        text = f'''
Информация о заказе
 ◉ Дата: {order.work_start.date()}
 ◉ Время: {order.work_start.time()}
 ◉ Адрес: {order.address}
    '''
        keyboard = get_staff_order_keyboard(order_id, staff_id)
        context.bot.edit_message_text(chat_id=chat_id, message_id=message_id, text=text, reply_markup=keyboard)
