from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse
from django.views.generic import CreateView, UpdateView, DeleteView

from crmapp.forms import ServiceOrderForm
from crmapp.models import ServiceOrder, Order


class ServiceOrderCreateView(CreateView):
    model = ServiceOrder
    template_name = 'service_order/service_order_create.html'
    form_class = ServiceOrderForm

    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        self.object = form.save(commit=False)
        self.object.total = self.object.service_total()
        self.object.order = order
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('crmapp:order_detail', kwargs={'pk': self.object.order.pk})


class ServiceOrderUpdateView(UpdateView):
    model = ServiceOrder
    template_name = 'service_order/service_order_update.html'
    form_class = ServiceOrderForm
    context_object_name = 'service_order'

    def form_valid(self, form):
        self.object.total = self.object.service_total()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('crmapp:order_detail', kwargs={'pk': self.object.order.pk})


class ServiceOrderDeleteView(DeleteView):
    model = ServiceOrder
    template_name = 'service_order/service_order_delete.html'
    context_object_name = 'service_order'

    def get_success_url(self):
        return reverse('crmapp:order_detail', kwargs={'pk': self.object.order.pk})
