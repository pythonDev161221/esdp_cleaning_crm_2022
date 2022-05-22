from django.contrib import messages
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, DetailView, FormView

from crmapp.crispy_form_helpers import OrderFormHelper, ServiceFormHelper, CleanersPartHelper, StaffFormHelper
from crmapp.forms import OrderForm, ServiceOrderForm, OrderStaffForm, CleanersPartForm
from crmapp.models import Order, ServiceOrder, StaffOrder


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_service'] = self.object.order_services.all()
        context['staff'] = self.object.order_cliners.all()
        return context


class FirstStepOrderCreateView(FormView):
    model = Order
    form_class = OrderForm
    formset = inlineformset_factory(
        Order,
        ServiceOrder,
        form=ServiceOrderForm,
        exclude=['order'],
        extra=3,
        can_delete=False
    )
    template_name = 'order/order_create.html'
    object = None

    def get_context_data(self, **kwargs):
        kwargs['formset'] = self.formset()
        kwargs['form_helper'] = OrderFormHelper()
        kwargs['formset_helper'] = ServiceFormHelper()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        formset = self.formset(self.request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset=None):
        form.instance.manager = self.request.user
        self.object = form.save()
        formset.instance = self.object
        formset.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset=None):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                formset=formset,
            )
        )

    def get_success_url(self):
        return reverse_lazy('crmapp:cleaners_add', kwargs={'pk': self.object.pk})


class CleanersAddView(FormView):
    model = Order
    form_class = CleanersPartForm
    formset = inlineformset_factory(
        Order,
        StaffOrder,
        form=OrderStaffForm,
        fields=['staff', 'is_brigadier'],
        extra=5,
        can_delete=False
    )
    template_name = 'order/cleaners_add.html'
    object = None

    def get_context_data(self, **kwargs):
        context = super(CleanersAddView, self).get_context_data(**kwargs)
        context['formset'] = self.formset()
        context['form_helper'] = CleanersPartHelper()
        context['formset_helper'] = StaffFormHelper()
        return context

    def post(self, request, *args, **kwargs):
        formset = self.formset(request.POST)
        form = self.form_class(request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset=None):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        order.cleaners_part = form.cleaned_data.get('cleaners_part')
        order.part_units = form.cleaned_data.get('part_units')
        order.save()
        formset.instance = order
        formset.save()
        messages.success(self.request, f'Заказ успешно создан!')
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, formset=None):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                formset=formset,
            )
        )

    def get_success_url(self):
        return reverse('crmapp:order_index')
