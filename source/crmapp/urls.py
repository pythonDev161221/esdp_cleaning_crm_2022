from django.urls import path

from crmapp.views.client_views import ClientCreateView

app_name = 'crmapp'

urlpatterns = [
    path('client/create/', ClientCreateView.as_view(), name='client_create')
]
