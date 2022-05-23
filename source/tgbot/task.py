from telegram import Update
from tgbot.dispatcher import dispatcher, bot


def process_telegram_event(update_json):
    update = Update.de_json(update_json, bot)
    dispatcher.process_update(update)