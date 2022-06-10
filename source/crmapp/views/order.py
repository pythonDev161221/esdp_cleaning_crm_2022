from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView

from crmapp.helpers.crispy_form_helpers import OrderFormHelper, ServiceFormHelper, CleanersPartHelper, StaffFormHelper
from crmapp.forms import CleanersPartForm, OrderForm, OrderCommentForm
from crmapp.helpers.order_helpers import BaseOrderCreateView, ServiceFormset, StaffFormset

from crmapp.models import Order, ForemanOrderUpdate, ForemanReport

from crmapp.views.search_view import SearchView

from tgbot.handlers.orders.tg_order_staff import staff_accept_order

User = get_user_model()


class OrderListView(PermissionRequiredMixin, SearchView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    ordering = 'work_start'
    search_fields = ["status__icontains", "work_start__icontains", "address__icontains"]
    permission_required = "crmapp.view_order"


class OrderDetailView(PermissionRequiredMixin, DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'
    permission_required = "crmapp.view_order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brigadir'] = self.object.order_cleaners.get(is_brigadier=True)
        return context


class FirstStepOrderCreateView(PermissionRequiredMixin, BaseOrderCreateView):
    model = Order
    form_class = OrderForm
    formset = ServiceFormset
    template_name = 'order/order_create.html'
    form_helper = OrderFormHelper
    formset_helper = ServiceFormHelper
    permission_required = "crmapp.add_order"

    def form_valid(self, form, formset=None):
        form.instance.manager = self.request.user
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse_lazy('crmapp:cleaners_add', kwargs={'pk': self.object.pk})


class SecondStepOrderCreateView(PermissionRequiredMixin, BaseOrderCreateView):
    model = Order
    form_class = CleanersPartForm
    template_name = 'order/cleaners_add.html'
    formset = StaffFormset
    form_helper = CleanersPartHelper
    formset_helper = StaffFormHelper
    permission_required = "crmapp.add_order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["formset"] = self.get_staff_filtered_formset(context["formset"])
        return context

    def form_valid(self, form, formset=None):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.cleaners_part = form.cleaned_data.get('cleaners_part')
        order.part_units = form.cleaned_data.get('part_units')
        order.save()
        formset.instance = order
        formset.save()
        staff_accept_order(order)
        messages.success(self.request, f'Заказ успешно создан!')
        return HttpResponseRedirect(self.get_success_url())

    def get_staff_filtered_formset(self, formset):
        order = get_object_or_404(Order, pk=self.kwargs.get("pk"))
        staff_filter = User.objects.filter(
            is_staff=False, is_active=True, black_list=False, schedule=order.work_start.isoweekday()
        ).exclude(
            Q(cleaner_orders__order=order) |
            Q(
                Q(cleaner_orders__order__work_start__gte=order.work_end) |
                Q(cleaner_orders__order__work_end__gte=order.work_start) &
                Q(cleaner_orders__order__work_end__gte=order.work_end)
            )
        )
        for form in formset:
            form.fields["staff"].queryset = staff_filter

        return formset

    def get_success_url(self):
        return reverse('crmapp:order_index')


class OrderCommentUpdate(PermissionRequiredMixin, UpdateView):
    model = Order
    form_class = OrderCommentForm
    template_name = 'order/order_finish.html'
    success_url = reverse_lazy('crmapp:order_index')

    def has_permission(self):
        return self.request.user == self.get_object().manager or self.request.user.is_staff