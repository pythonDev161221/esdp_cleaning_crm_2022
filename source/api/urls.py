from django.urls import path

from api.views import get_token_view, ApiClientCreateView

app_name = 'api'

urlpatterns = [
    path('get-csrf-token/', get_token_view),
    path("client/create/", ApiClientCreateView.as_view()),
]