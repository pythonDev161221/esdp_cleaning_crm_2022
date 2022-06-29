from django.contrib.auth.mixins import PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView

from crmapp.forms import ServiceOrderForm
from crmapp.models import ServiceOrder, Order


class ServiceOrderCreateView(PermissionRequiredMixin, CreateView):
    model = ServiceOrder
    template_name = 'service_order/service_order_create.html'
    success_url = reverse_lazy('crmapp:service_order_create')
    form_class = ServiceOrderForm
    permission_required = "crmapp.add_serviceorder"

    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        self.object = form.save(commit=False)
        self.object.total = self.object.service_total()
        self.object.order = order
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('crmapp:order_detail', kwargs={'pk': self.object.order.pk})

    def has_permission(self):
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        return self.request.user == order.manager and super().has_permission() or self.request.user.is_staff or self.request.user == order.order_cleaners.get(
            is_brigadier=True).staff


class ServiceOrderUpdateView(PermissionRequiredMixin, UpdateView):
    model = ServiceOrder
    template_name = 'service_order/service_order_update.html'
    form_class = ServiceOrderForm
    context_object_name = 'service_order'
    permission_required = "crmapp.change_serviceorder"

    def form_valid(self, form):
        self.object.total = self.object.service_total()
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('crmapp:order_detail', kwargs={'pk': self.object.order.pk})

    def has_permission(self):
        order = get_object_or_404(Order, pk=self.kwargs.get("pk"))
        return self.request.user == order.manager and super().has_permission() or self.request.user == order.order_cleaners.filter(
            is_brigadier=True).staff or self.request.user.is_staff


class ServiceOrderDeleteView(PermissionRequiredMixin, DeleteView):
    model = ServiceOrder
    template_name = 'service_order/service_order_delete.html'
    context_object_name = 'service_order'
    permission_required = "crmapp.delete_serviceorder"

    def get_success_url(self):
        return reverse('crmapp:order_detail', kwargs={'pk': self.object.order.pk})

    def has_permission(self):
        return self.request.user == self.get_object().order.manager and super().has_permission() or self.request.user.is_staff
