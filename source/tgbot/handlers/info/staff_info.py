from django.contrib.auth import get_user_model
from telegram import Update, bot
from telegram.ext import CallbackContext

User = get_user_model()


def info(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    user = User.objects.get(telegram_id=chat_id)
    sсhedule_list = []
    wallet_list = []
    if user.experience == 'trainee':
        user.experience = 'Стажер'
    elif user.experience == 'skilled':
        user.experience = 'Опытный'
    elif user.experience == 'expert':
        user.experience = 'Профессионал'
    for day in user.schedule.all():
        sсhedule_list.append(day)
    working_days = ', '.join(map(str, sсhedule_list))
    for item in user.online_wallet:
        wallet_list.append(item)
    wallet = '\n'.join(map(str, wallet_list))
    text = f'''
ФИО: {user.first_name} {user.last_name} ({user.experience})
ИНН: {user.inn_passport}
Телефон: {user.phone}
Адрес: {user.address}
Рабочие дни: {working_days}
Электронные кошельки:\n{wallet}'''
    context.bot.send_message(chat_id, text=text)
