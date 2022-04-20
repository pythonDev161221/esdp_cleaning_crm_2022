from django.urls import path, include

from crmapp.views.client_views import ClientCreateView, ClientListView, ClientUpdateView
from crmapp.views.consumables import InventoryListView, InventoryCreateView, InventoryUpdateView, InventoryDeleteView

app_name = 'crmapp'

client_urlpatterns = [
    path('all/', ClientListView.as_view(), name='client_index'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('up/<int:pk>', ClientUpdateView.as_view(), name='client_update')
]

consumables_urlpatterns = [
    path('inventory/all/', InventoryListView.as_view(), name='inventory_index'),
    path('inventory/create/', InventoryCreateView.as_view(), name='inventory_create'),
    path('inventory/up/<int:pk>/', InventoryUpdateView.as_view(), name='inventory_update'),
    path('inventory/delete/<int:pk>/', InventoryDeleteView.as_view(), name='inventory_delete')
]

urlpatterns = [
    path('client/', include(client_urlpatterns)),
    path('consumables/', include(consumables_urlpatterns))
]

