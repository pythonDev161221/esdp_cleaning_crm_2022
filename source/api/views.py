from django.http import HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView

from api.serializers import ClientSerializer, OrderServiceSerializer, ServiceListSerializer
from crmapp.models import Client, ServiceOrder, Service


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ApiClientCreateView(CreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ApiServiceOrderUpdate(RetrieveUpdateAPIView):
    serializer_class = OrderServiceSerializer
    queryset = ServiceOrder.objects.all()


class ApiServiceOrderDelete(DestroyAPIView):
    serializer_class = OrderServiceSerializer
    queryset = ServiceOrder.objects.all()