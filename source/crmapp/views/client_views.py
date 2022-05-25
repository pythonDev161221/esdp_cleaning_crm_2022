from django.views.generic import CreateView, ListView, UpdateView

from crmapp.forms import ClientForm
from crmapp.models import Client


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'


class ClientListView(ListView):
    model = Client
    template_name = 'client/client_index.html'
    context_object_name = 'clients'


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'
