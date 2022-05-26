from django.contrib.auth import get_user_model
from telegram import Update
from telegram.ext import CallbackContext

User = get_user_model()


def start_and_auth(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    text = update.message.text
    try:
        command, auth_token = text.split(" ")
        if User.objects.filter(telegram_auth_token=auth_token):
            u = User.objects.get(telegram_auth_token=auth_token)
            u.telegram_id = chat_id
            u.telegram_auth_token = None
            u.save()
            context.bot.send_message(chat_id, f"Вы успешно авторизовались {u.last_name} {u.first_name}")
        else:
            context.bot.send_message(chat_id, "Данная ссылка недействительна")
    except:
        if not User.objects.filter(telegram_id=chat_id):
            context.bot.send_message(chat_id, "Вы не можете пользоваться данным ботом")
