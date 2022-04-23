from django.urls import path, include

from crmapp.views.client_views import ClientCreateView, ClientListView, ClientUpdateView


from crmapp.views.service_views import ServiceListView, ServiceCreateView, ServiceUpdateView, ServiceDeleteView, \
    PropertySortListView, PropertySortCreateView, PropertySortUpdateView, PropertySortDeleteView, CleaningSortListView, \
    CleaningSortCreateView, CleaningSortUpdateView, CleaningSortDeleteView

from crmapp.views.consumables import InventoryListView, InventoryCreateView, InventoryUpdateView, InventoryDeleteView, \
    CleansearListView, CleansearCreateView, CleansearUpdateView, CleansearDeleteView, CleansearDetailView
from crmapp.views.extra_service_views import ExtraServiceListView, ExtraServiceCreateView, ExtraServiceUpdateView, ExtraServiceDeleteView
from crmapp.views.servie_views import ServiceOrderListView, ServiceOrderDetailView, ServiceOrderCreateView, \
    ServiceOrderUpdateView, ServiceOrderDeleteView

app_name = 'crmapp'

client_urlpatterns = [
    path('all/', ClientListView.as_view(), name='client_index'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('up/<int:pk>', ClientUpdateView.as_view(), name='client_update')
]

service_urlpatterns = [
    path('list/', ServiceListView.as_view(), name='service_list'),
    path('create/', ServiceCreateView.as_view(), name='service_create'),
    path('update/<int:pk>/', ServiceUpdateView.as_view(), name='service_update'),
    path('delete/<int:pk>/', ServiceDeleteView.as_view(), name='service_delete'),
]

property_sort_urlpatterns = [
    path('list/', PropertySortListView.as_view(), name='property_sort_list'),
    path('create/', PropertySortCreateView.as_view(), name='property_sort_create'),
    path('update/<int:pk>/', PropertySortUpdateView.as_view(), name='property_sort_update'),
    path('delete/<int:pk>/', PropertySortDeleteView.as_view(), name='property_sort_delete'),
]

cleaning_sort_urlpatterns = [
    path('list/', CleaningSortListView.as_view(), name='cleaning_sort_list'),
    path('create/', CleaningSortCreateView.as_view(), name='cleaning_sort_create'),
    path('update/<int:pk>/', CleaningSortUpdateView.as_view(), name='cleaning_sort_update'),
    path('delete/<int:pk>/', CleaningSortDeleteView.as_view(), name='cleaning_sort_delete'),
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

service_order_urlpatterns = [
    path("", ServiceOrderListView.as_view(), name="service_order_list"),
    path("detail/<int:pk>/", ServiceOrderDetailView.as_view(), name="service_order_detail"),
    path("create/", ServiceOrderCreateView.as_view(), name="service_order_create"),
    path("update/<int:pk>/", ServiceOrderUpdateView.as_view(), name="service_order_update"),
    path("delete/<int:pk>/", ServiceOrderDeleteView.as_view(), name="service_order_delete"),
]

urlpatterns = [
    path('client/', include(client_urlpatterns)),
    path('service/', include(service_urlpatterns)),
    path('property_sort/', include(property_sort_urlpatterns)),
    path('cleaning_sort/', include(cleaning_sort_urlpatterns)),
    path('extra-service/', include(extra_service_urlpatterns)),
    path('service_order/', include(service_order_urlpatterns)),
    path('consumables/', include(consumables_urlpatterns)),
]

