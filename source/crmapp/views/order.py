from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import PermissionRequiredMixin
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import DetailView, UpdateView, DeleteView, ListView

from crmapp.helpers.crispy_form_helpers import OrderFormHelper, ServiceFormHelper, CleanersPartHelper, StaffFormHelper
from crmapp.forms import CleanersPartForm, OrderForm, OrderCommentForm
from crmapp.helpers.order_helpers import BaseOrderCreateView, ServiceFormset, StaffFormset

from crmapp.models import Order, ForemanOrderUpdate

from tgbot.handlers.orders.tg_order_staff import staff_accept_order, order_finished, manager_alert, order_canceled

from crmapp.forms import SearchForm

User = get_user_model()


class OrderListView(PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'
    permission_required = "crmapp.view_order"
    search_form_class = SearchForm

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value = self.get_search_value()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = Order.objects.order_by('work_start').exclude(is_deleted=True)
        if self.search_value:
            query = Q(status__icontains=self.search_value) | Q(work_start__icontains=self.search_value) | Q(
                address__icontains=self.search_value)
            queryset = queryset.filter(query)
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.search_form_class()
        return context

    def get_form(self):
        return self.search_form_class(self.request.GET)

    def get_search_value(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("search")


class OrderDetailView(PermissionRequiredMixin, DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'
    permission_required = "crmapp.view_order"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['brigadir'] = self.object.order_cleaners.get(is_brigadier=True)
        return context

    def has_permission(self):
        return super().has_permission() or self.get_object().order_cleaners.get(is_brigadier=True).staff == self.request.user


class OrderDeleteView(PermissionRequiredMixin, DeleteView):
    model = Order
    success_url = reverse_lazy('crmapp:order_index')
    template_name = 'order/order_delete.html'
    context_object_name = 'order'

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        self.object.soft_delete()
        messages.success(self.request, f'Заказ № {self.object.pk} успешно удален!')
        return HttpResponseRedirect(self.get_success_url())

    def has_permission(self):
        return self.request.user == self.get_object().manager or self.request.user.is_staff


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


class OrderUpdateView(UpdateView):
    model = Order
    template_name = 'order/order_update.html'
    form_class = OrderForm
    form_helper = OrderFormHelper

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form_helper'] = self.form_helper()
        print(context)
        return context

    def get_success_url(self):
        return reverse('crmapp:order_detail', kwargs={'pk': self.object.pk})


class OrderFinishView(PermissionRequiredMixin, UpdateView):
    model = Order
    form_class = OrderCommentForm
    template_name = 'order/order_finish.html'
    success_url = reverse_lazy('crmapp:order_index')

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        if request.method == 'POST' and 'finish' in request.POST:
            order.finish_order()
            order_finished(order)
        elif request.method == 'POST' and 'cancel' in request.POST:
            order.cancel_order()
            order_canceled(order)
        return super(OrderFinishView, self).post(request, **kwargs)

    def form_valid(self, form, formset=None):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.description = form.cleaned_data.get('description')
        order.save()
        messages.success(self.request, f'Статус заказа №{order.id} изменен на "{order.get_status_display()}"')
        return HttpResponseRedirect(self.get_success_url())

    def has_permission(self):
        return self.request.user == self.get_object().manager or self.request.user.is_staff


class OrderDeletedListView(PermissionRequiredMixin, ListView):
    model = Order
    template_name = 'order/order_deleted_list.html'
    context_object_name = "orders"
    permission_required = "crmapp:can_view_order_deleted_list"

    def get_queryset(self):
        queryset = Order.objects.filter(is_deleted=True)
        return queryset
