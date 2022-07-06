import json
import logging
import threading
from django.views import View
from django.http import JsonResponse

from tgbot.dispatcher import TELEGRAM_BOT_USERNAME
from tgbot.task import process_telegram_event

logger = logging.getLogger(__name__)

BOT_URL = f"https://t.me/{TELEGRAM_BOT_USERNAME}"


class TelegramBotWebhookView(View):
    # WARNING: if fail - Telegram webhook will be delivered again.
    # Can be fixed with async celery task execution
    def post(self, request, *args, **kwargs):
        thr = threading.Thread(target=process_telegram_event, args=(json.loads(request.body),))
        thr.start()
        return JsonResponse({"ok": "POST request processed"})

    def get(self, request, *args, **kwargs):  # for debug
        return JsonResponse({"ok": "Get request processed. But nothing done"})