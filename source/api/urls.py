from django.urls import path

from api.views import get_token_view, ApiClientCreateView, ApiServiceOrderUpdate, ApiServiceOrderDelete

app_name = 'api'

urlpatterns = [
    path('get-csrf-token/', get_token_view),
    path("client/create/", ApiClientCreateView.as_view()),
    path('update/service/<int:pk>', ApiServiceOrderUpdate.as_view()),
    path('delete/service/<int:pk>', ApiServiceOrderDelete.as_view())
]
