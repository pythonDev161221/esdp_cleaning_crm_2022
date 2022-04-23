from django.http import HttpResponseRedirect
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView

from crmapp.forms import ServiceOrderForm
from crmapp.models import ServiceOrder


class ServiceOrderListView(ListView):
    model = ServiceOrder
    template_name = 'service/service_order/service_order_list.html'
    context_object_name = 'service_orders'


class ServiceOrderDetailView(DetailView):
    model = ServiceOrder
    template_name = 'service/service_order/service_order_detail.html'
    context_object_name = 'service_order'


class ServiceOrderCreateView(CreateView):
    model = ServiceOrder
    template_name = 'service/service_order/service_order_create.html'
    form_class = ServiceOrderForm

    def form_valid(self, form):
        form.instance.total = form.instance.service.price * form.instance.amount * form.instance.rate
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('crmapp:service_order_detail', kwargs={'pk': self.object.pk})


class ServiceOrderUpdateView(UpdateView):
    model = ServiceOrder
    template_name = 'service/service_order/service_order_update.html'
    form_class = ServiceOrderForm
    context_object_name = 'service_order'

    def form_valid(self, form):
        form.instance.total = form.instance.service.price * form.instance.amount * form.instance.rate
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('crmapp:service_order_detail', kwargs={'pk': self.object.pk})


class ServiceOrderDeleteView(DeleteView):
    model = ServiceOrder
    template_name = 'service/service_order/service_order_delete.html'
    success_url = reverse_lazy('crmapp:service_order_list')
    context_object_name = 'service_order'
