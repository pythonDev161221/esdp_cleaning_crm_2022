import json
import logging
from django.views import View
from django.http import JsonResponse

from main.settings import DEBUG

from tgbot.dispatcher import process_telegram_event, TELEGRAM_BOT_USERNAME

logger = logging.getLogger(__name__)

BOT_URL = f"https://t.me/{TELEGRAM_BOT_USERNAME}"


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        if DEBUG:
            process_telegram_event(json.loads(request.body))
        else:  # use celery in production
            process_telegram_event.delay(json.loads(request.body))

        # e.g. remove buttons
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request processed. But nothing done"})