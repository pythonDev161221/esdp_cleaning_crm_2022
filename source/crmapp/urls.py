from django.urls import path, include

from crmapp.views.client_views import ClientCreateView, ClientListView, ClientUpdateView
from crmapp.views.extra_service_views import ExtraServiceListView, ExtraServiceCreateView, ExtraServiceUpdateView, ExtraServiceDeleteView


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

urlpatterns = [
    path('client/', include(client_urlpatterns)),
    path('extra-service/', include(extra_service_urlpatterns))
]

