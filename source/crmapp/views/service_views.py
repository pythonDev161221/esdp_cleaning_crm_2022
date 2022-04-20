from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from crmapp.forms import ServiceForm
from crmapp.models import Service


class ServiceListView(ListView):
    model = Service
    template_name = 'service/list.html'
    context_object_name = 'services'


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/create.html'
    success_url = reverse_lazy('crmapp:service_list')


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/update.html'

    def get_success_url(self):
        return reverse("crmapp:service_list")


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service/delete.html'
    success_url = reverse_lazy('crmapp:service_list')
