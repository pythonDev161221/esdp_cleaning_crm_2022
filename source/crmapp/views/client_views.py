from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import CreateView, UpdateView

from crmapp.forms import ClientForm
from crmapp.models import Client

from crmapp.views.search_view import SearchView


class ClientCreateView(PermissionRequiredMixin, CreateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_create.html'
    permission_required = "crmapp.add_client"


class ClientListView(PermissionRequiredMixin, SearchView):
    model = Client
    template_name = 'client/client_list.html'
    context_object_name = 'clients'
    permission_required = "crmapp.view_client"
    search_fields = ["first_name__icontains", "last_name__icontains", "organization__icontains", "phone__icontains"]


class ClientUpdateView(PermissionRequiredMixin, UpdateView):
    model = Client
    form_class = ClientForm
    template_name = 'client/client_create.html'
    permission_required = "crmapp.change_client"
