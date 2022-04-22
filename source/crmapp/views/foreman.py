from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect, render
from django.views import View
from django.views.generic import CreateView

from crmapp.forms import ForemanService, ForemanService, ForemanExtraService
from crmapp.models import ForemanOrderUpdate, Order, ServiceOrder, ExtraServiceOrder


class ForemanOrderUpdateCreateView(View):
    model = ForemanOrderUpdate
    template_name = 'foreman/create_order_update.html'
    ServiceFormSet = modelformset_factory(ServiceOrder, fields=('service', 'amount', 'rate', 'total'))
    ExtraFormSet = modelformset_factory(ExtraServiceOrder, fields=('extra_service', 'amount', 'rate', 'total'))


    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        # print(f'order_get = {order}')
        service_formset = self.ServiceFormSet(queryset=order.service.all(), prefix='service')
        extra_formset = self.ExtraFormSet(queryset=order.extra_service.all(), prefix='extra')
        return render(request, self.template_name, {'service_form': service_formset, 'extra_service_form' : extra_formset})


    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        # ServiceFormSet = modelformset_factory(ServiceOrder, form=ForemanService)
        service_form = self.ServiceFormSet(request.POST, prefix='service')
        services = service_form.save(commit=True)
        print(f'services {services}')
        # print(service_form)
        print(f'request {request.POST}')

        if service_form.is_valid():
            print('OK')
        # print(f'service_form = {service_form}')
        # extra_service_form = self.ExtraFormSet(request.POST)
        # print(f'extra service = {extra_service_form}')
        # if service_form.is_valid():
        #     print('after if', service_form)
        # if service_form.is_valid() and extra_service_form.is_valid():
        #     return self.form_valid(form, service_form, extra_service_form)
            # service = service_form.save(commit=False)
            # extra = extra_service_form.save(commit=False)
            # service.save()
            # extra.save()
            # foreman_order = ForemanOrderUpdate.objects.get_or_create(order_id=1, extra_service=extra)
        return redirect('crmapp:foremanorder_create', 1)


    # def get_context_data(self, **kwargs):
    #     print('getcontext', kwargs)
    #     order = Order.objects.first()
    #
    #
    #     if 'service_form' not in kwargs and 'extra_service_form' not in kwargs:
    #         kwargs['service_form'] = service_formset
    #         kwargs['extra_service_form'] = extra_formset
    #     return super().get_context_data(**kwargs)

    # def get(self, request, *args, **kwargs):
        # print(kwargs)
        # self.get_context_data()

    # def form_valid(self, form, service_form, extra_service_form):
    #     service = service_form.save()
    #     extra = extra_service_form.save()
    #     foreman = form.save(commit=False)
    #     foreman.service = service
    #     foreman.extra_service = extra
    #     foreman.order_id = 1
    #     foreman.save()
    #     print(foreman)
    #     return super().form_valid(form)
        # print(service)
        # print(extra)
        # print(form_)

    # def post(self, request, *args, **kwargs):
    #     form = self.get_form()
    #     profile_form = self.get_profile_form()
    #     if form.is_valid() and profile_form.is_valid():
    #         return self.form_valid(form, profile_form)
    #     else:
    #         return self.form_invalid(form, profile_form)
    #
    # def form_valid(self, form, profile_form):
    #     profile_form.save()
    #     return super().form_valid(form)

    # def get_service_form(self):
    #     form_kwargs = {}
    #     if self.request.method == 'POST':
    #         form_kwargs['data'] = self.request.POST
    #     return ForemanService(**form_kwargs)
    #
    # def get_extra_form(self):
    #     form_kwargs = {}
    #     if self.request.method == 'POST':
    #         form_kwargs['data'] = self.request.POST

    def get_success_url(self):
        return redirect('crmapp:foremanupdate_create')
