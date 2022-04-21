from django.urls import path, include

from crmapp.views.client_views import ClientCreateView, ClientListView, ClientUpdateView
from crmapp.views.consumables import InventoryListView, InventoryCreateView, InventoryUpdateView, InventoryDeleteView, \
    CleansearListView, CleansearCreateView, CleansearUpdateView, CleansearDeleteView, CleansearDetailView
from crmapp.views.extra_service_views import ExtraServiceListView, ExtraServiceCreateView, ExtraServiceUpdateView, ExtraServiceDeleteView


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
    path('inventory/delete/<int:pk>/', InventoryDeleteView.as_view(), name='inventory_delete'),

    path('cleansear/all/', CleansearListView.as_view(), name='cleansear_index'),
    path('cleansear/create/', CleansearCreateView.as_view(), name='cleansear_create'),
    path('cleansear/up/<int:pk>/', CleansearUpdateView.as_view(), name='cleansear_update'),
    path('cleansear/delete/<int:pk>/', CleansearDeleteView.as_view(), name='cleansear_delete'),
    path('cleansear/detail/<int:pk>/', CleansearDetailView.as_view(), name='cleansear_detail')
]



extra_service_urlpatterns = [
    path("", ExtraServiceListView.as_view(), name="extra_service_index"),
    path("create/", ExtraServiceCreateView.as_view(), name="extra_service_create"),
    path("<int:pk>/update/", ExtraServiceUpdateView.as_view(), name="extra_service_update"),
    path("<int:pk>/delete/", ExtraServiceDeleteView.as_view(), name="extra_service_delete")
]

urlpatterns = [
    path('client/', include(client_urlpatterns)),
    path('extra-service/', include(extra_service_urlpatterns)),
    path('consumables/', include(consumables_urlpatterns)),
]

