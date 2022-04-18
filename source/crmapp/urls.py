from django.urls import path

from crmapp.views.client_views import ClientCreateView, ClientListView, ClientUpdateView

app_name = 'crmapp'

urlpatterns = [
    path('client/create/', ClientCreateView.as_view(), name='client_create'),
    path('clients/', ClientListView.as_view(), name='client_index'),
    path('client/up/<int:pk>', ClientUpdateView.as_view(), name='client_update')
]
