from django.urls import path, include

from crmapp.views.client_views import ClientCreateView, ClientListView, ClientUpdateView
from crmapp.views.extra_service_views import ExtraServiceListView, ExtraServiceCreateView, ExtraServiceUpdateView, ExtraServiceDeleteView
from crmapp.views.servie_views import ServiceOrderListView, ServiceOrderDetailView, ServiceOrderCreateView, \
    ServiceOrderUpdateView, ServiceOrderDeleteView

app_name = 'crmapp'

client_urlpatterns = [
    path('all/', ClientListView.as_view(), name='client_index'),
    path('create/', ClientCreateView.as_view(), name='client_create'),
    path('up/<int:pk>', ClientUpdateView.as_view(), name='client_update')
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
    path('extra-service/', include(extra_service_urlpatterns)),
    path('service_order/', include(service_order_urlpatterns)),
]

