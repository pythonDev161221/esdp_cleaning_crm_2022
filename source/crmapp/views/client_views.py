from django.views.generic import CreateView

from accounts.forms import ClientForm
from crmapp.models import Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_create.html'

