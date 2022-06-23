from django.urls import path

from api_v1.views import get_token_view, ApiFineCreateView, ApiBonusCreateView, ApiInventoryCreateView, ApiObjectTypeCreateView

app_name = 'api'

urlpatterns = [
    path('get-csrf-token/', get_token_view),
    path('fine/create/', ApiFineCreateView.as_view()),
    path('bonus/create/', ApiBonusCreateView.as_view()),
    path('inventory/create/', ApiInventoryCreateView.as_view()),
    path('object_type/create/', ApiObjectTypeCreateView.as_view()),
]