from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from crmapp.models import ExtraService
from crmapp.forms import ExtraServiceForm


class ExtraServiceListView(ListView):
    model = ExtraService
    template_name = "extra_service/extra_service_list.html"
    context_object_name = "extra_servises"


class ExtraServiceCreateView(CreateView):
    model = ExtraService
    form_class = ExtraServiceForm
    template_name = "extra_service/create.html"

    def get_success_url(self):
        return reverse("crmapp:extra_service_index")


class ExtraServiceUpdateView(UpdateView):
    model = ExtraService
    form_class = ExtraServiceForm
    template_name = "extra_service/update.html"

    def get_success_url(self):
        return reverse("crmapp:extra_service_index")


class ExtraServiceDeleteView(DeleteView):
    model = ExtraService
    template_name = "extra_service/delete.html"

    def get_success_url(self):
        return reverse("crmapp:extra_service_index")