from django.http import HttpResponseNotAllowed, HttpResponse
from django.views.decorators.csrf import ensure_csrf_cookie
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveUpdateAPIView, DestroyAPIView

from api.serializers import ClientSerializer
from crmapp.models import Client


@ensure_csrf_cookie
def get_token_view(request, *args, **kwargs):
    if request.method == 'GET':
        return HttpResponse()
    return HttpResponseNotAllowed('Only GET request are allowed')


class ApiClientCreateView(CreateAPIView):
    serializer_class = ClientSerializer
    queryset = Client.objects.all()
