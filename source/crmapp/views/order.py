from django.contrib import messages
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView

from crmapp.helpers.crispy_form_helpers import OrderFormHelper, ServiceFormHelper, CleanersPartHelper, StaffFormHelper
from crmapp.forms import CleanersPartForm, OrderForm
from crmapp.helpers.order_helpers import BaseOrderCreateView, ServiceFormset, StaffFormset

from crmapp.models import Order, ForemanOrderUpdate, ForemanReport


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    ordering = '-created_at'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_service'] = self.object.order_services.all()
        context['staff'] = self.object.order_cleaners.all()
        context['brigadir'] = self.object.order_cleaners.get(is_brigadier=True)
        try:
            foreman_update = ForemanOrderUpdate.objects.get(order_id=self.object.pk)
            foreman_report = ForemanReport.objects.get(order_id=self.object.pk)
            foreman_expenses = foreman_report.foreman_expense.all()
            context['foreman_update'] = foreman_update
            context['foreman_expenses'] = foreman_expenses
            return context
        except:
            return context


class FirstStepOrderCreateView(BaseOrderCreateView):
    model = Order
    form_class = OrderForm
    formset = ServiceFormset
    template_name = 'order/order_create.html'
    form_helper = OrderFormHelper
    formset_helper = ServiceFormHelper

    def form_valid(self, form, formset=None):
        form.instance.manager = self.request.user
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('crmapp:cleaners_add', kwargs={'pk': self.object.pk})


class SecondStepOrderCreateView(BaseOrderCreateView):
    model = Order
    form_class = CleanersPartForm
    template_name = 'order/cleaners_add.html'
    formset = StaffFormset
    form_helper = CleanersPartHelper
    formset_helper = StaffFormHelper

    def form_valid(self, form, formset=None):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.cleaners_part = form.cleaned_data.get('cleaners_part')
        order.part_units = form.cleaned_data.get('part_units')
        order.save()
        formset.instance = order
        formset.save()
        messages.success(self.request, f'Заказ успешно создан!')
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('crmapp:order_index')
