from functools import wraps
from typing import Callable

from django.contrib.auth import get_user_model
from crmapp.models import Order


def is_authenticated_telegram(func: Callable):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        if get_user_model().objects.filter(telegram_id=update.message.chat_id):
            return func(update, context,  *args, **kwargs)
        else:
            return
    return command_func


def is_staff_in_order(func: Callable):
    @wraps(func)
    def command_func(update, context, *args, **kwargs):
        chat_id = update.callback_query.message.chat.id
        message_id = update.callback_query.message.message_id
        try:
            call, order_id, staff_id = update.callback_query.data.split(" ")
            Order.objects.get(pk=order_id).order_cleaners.get(staff=staff_id)
            return func(update, context,  *args, **kwargs)
        except:
            text = f"Вы были удалены с данного заказа!"
            context.bot.delete_message(chat_id=chat_id, message_id=message_id)
            context.bot.send_message(chat_id=chat_id, text=text)
            return
    return command_func