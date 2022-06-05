from django.contrib.auth import get_user_model
from telegram import Update, bot
from telegram.ext import CallbackContext


User = get_user_model()


def balance(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user = User.objects.get(telegram_id=chat_id)
    text = f'Ваш баланс состаляет {user.balance} сом, cэр!'
    context.bot.send_message(chat_id, text=text)
