from django.urls import reverse_lazy, reverse
from django.views.generic import CreateView, ListView, UpdateView, DeleteView, DetailView

from crmapp.forms import ServiceForm, PropertySortForm, CleaningSortForm
from crmapp.models import Service, PropertySort, CleaningSort


class ServiceListView(ListView):
    model = Service
    template_name = 'service/service/service_list.html'
    context_object_name = 'services'


class ServiceCreateView(CreateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/service/service_create.html'
    success_url = reverse_lazy('crmapp:service_list')


class ServiceUpdateView(UpdateView):
    model = Service
    form_class = ServiceForm
    template_name = 'service/service/service_update.html'

    def get_success_url(self):
        return reverse("crmapp:service_list")


class ServiceDeleteView(DeleteView):
    model = Service
    template_name = 'service/service/service_delete.html'
    success_url = reverse_lazy('crmapp:service_list')


class PropertySortListView(ListView):
    model = PropertySort
    context_object_name = 'property_sorts'
    template_name = 'service/property_sort/property_sort_list.html'


class PropertySortCreateView(CreateView):
    model = PropertySort
    form_class = PropertySortForm
    success_url = reverse_lazy('crmapp:property_sort_list')
    template_name = 'service/property_sort/property_sort_create.html'


class PropertySortUpdateView(UpdateView):
    model = PropertySort
    form_class = PropertySortForm
    template_name = 'service/property_sort/property_sort_update.html'
    success_url = reverse_lazy('crmapp:property_sort_list')


class PropertySortDeleteView(DeleteView):
    model = PropertySort
    template_name = 'service/property_sort/property_sort_delete.html'
    context_object_name = 'property_sort'
    success_url = reverse_lazy('crmapp:property_sort_list')


class CleaningSortListView(ListView):
    model = CleaningSort
    context_object_name = 'cleaning_sorts'
    template_name = 'service/cleaning_sort/cleaning_sort_list.html'


class CleaningSortCreateView(CreateView):
    model = CleaningSort
    form_class = CleaningSortForm
    success_url = reverse_lazy('crmapp:cleaning_sort_list')
    template_name = 'service/cleaning_sort/cleaning_sort_create.html'


class CleaningSortUpdateView(UpdateView):
    model = CleaningSort
    form_class = CleaningSortForm
    success_url = reverse_lazy('crmapp:cleaning_sort_list')
    template_name = 'service/cleaning_sort/cleaning_sort_update.html'


class CleaningSortDeleteView(DeleteView):
    model = CleaningSort
    success_url = reverse_lazy('crmapp:cleaning_sort_list')
    context_object_name = 'cleaning_sort'
    template_name = 'service/cleaning_sort/cleaning_sort_delete.html'