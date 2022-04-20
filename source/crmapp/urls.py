from django.urls import path, include

from crmapp.views.client_views import ClientCreateView, ClientListView, ClientUpdateView
from crmapp.views.service_views import ServiceListView, ServiceCreateView, ServiceUpdateView, ServiceDeleteView, \
    PropertySortListView, PropertySortCreateView, PropertySortUpdateView, PropertySortDeleteView

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

urlpatterns = [
    path('client/', include(client_urlpatterns)),
    path('service/', include(service_urlpatterns)),
    path('property_sort/', include(property_sort_urlpatterns)),
]

