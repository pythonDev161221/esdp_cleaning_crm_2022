from django.urls import path
from django.views.decorators.csrf import csrf_exempt

from tgbot.views import TelegramBotWebhookView

urlpatterns = [
    path('cleaning-serice-bot/update/', csrf_exempt(TelegramBotWebhookView.as_view()))
]