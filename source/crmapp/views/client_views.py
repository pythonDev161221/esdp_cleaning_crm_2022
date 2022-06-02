from django.views.generic import CreateView, UpdateView

from crmapp.forms import ClientForm
from crmapp.models import Client

from crmapp.views.search_view import SearchView


class ClientCreateView(CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'


class ClientListView(SearchView):
    model = Client
    template_name = 'client/client_index.html'
    context_object_name = 'clients'
    search_fields = ["first_name__icontains", "last_name__icontains", "organization__icontains", "phone__icontains"]


class ClientUpdateView(UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_form.html'
