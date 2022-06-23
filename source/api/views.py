from django.http import HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView

from api.serializers import ClientSerializer, FineSerializer, BonusSerializer, InventorySerializer, ObjectTypeSerializer
from crmapp.models import Client, Fine, Bonus, Inventory, ObjectType


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ApiClientCreateView(CreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()


class ApiFineCreateView(CreateAPIView):
    serializer_class = FineSerializer
    queryset = Fine.objects.all()


class ApiBonusCreateView(CreateAPIView):
    serializer_class = BonusSerializer
    queryset = Bonus.objects.all()


class ApiInventoryCreateView(CreateAPIView):
    serializer_class = InventorySerializer
    queryset = Inventory.objects.all()


class ApiObjectTypeCreateView(CreateAPIView):
    serializer_class = ObjectTypeSerializer
    queryset = ObjectType.objects.all()
