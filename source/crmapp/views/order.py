from django.contrib import messages
from django.db import transaction
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView

from crmapp.forms import OrderForm, ServiceOrderFormSet, StaffOrderFormSet
from crmapp.models import Order, ForemanOrderUpdate, ForemanReport

from crmapp.views.search_view import SearchView

from tgbot.handlers.orders.tg_order_staff import staff_accept_order


class OrderListView(SearchView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    ordering = '-created_at'
    search_fields = ["status__icontains", "work_start__icontains", "address__icontains"]


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
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


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_create.html'
    success_url = 'crmapp:order_index'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        if self.request.POST:
            context['cliners'] = StaffOrderFormSet(self.request.POST)
            context['services'] = ServiceOrderFormSet(self.request.POST)
        else:
            context['cliners'] = StaffOrderFormSet()
            context['services'] = ServiceOrderFormSet()
        return context

    def form_valid(self, form):
        context = self.get_context_data()
        services = context['services']
        cliners = context['cliners']
        with transaction.atomic():
            self.object = form.save()
            if services.is_valid() and cliners.is_valid():
                cliners.instance = self.object
                services.instance = self.object
                cliners.save()
                services.save()
                staff_accept_order(self.object)
                messages.success(self.request, f'Заказ успешно создан!')
        return super(OrderCreateView, self).form_valid(form)

    def get_success_url(self):
        return reverse_lazy('crmapp:order_index')
