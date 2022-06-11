from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from crmapp.forms import ServiceForm
from crmapp.models import Service

from crmapp.views.search_view import SearchView


class ServiceListView(PermissionRequiredMixin, SearchView):
    model = Service
    template_name = 'service/service_list.html'
    context_object_name = 'services'
    search_fields = ["name__icontains"]
    permission_required = "crmapp.view_service"


class ServiceCreateView(PermissionRequiredMixin, CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/service_create.html'
    success_url = reverse_lazy('crmapp:service_list')
    permission_required = "crmapp.add_service"


class ServiceUpdateView(PermissionRequiredMixin, UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/service_update.html'
    permission_required = "crmapp.change_service"

    def get_success_url(self):
        return reverse("crmapp:service_list")


class ServiceDeleteView(PermissionRequiredMixin, DeleteView):
    model = Service
    template_name = 'service/service_delete.html'
    success_url = reverse_lazy('crmapp:service_list')
    permission_required = "crmapp.delete_service"
