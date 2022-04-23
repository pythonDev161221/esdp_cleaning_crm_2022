from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.views import View

from crmapp.forms import ForemanService, ForemanExtraService
from crmapp.models import ForemanOrderUpdate, Order, ServiceOrder, ExtraServiceOrder


class ForemanOrderUpdateCreateView(View):
    model = ForemanOrderUpdate
    template_name = 'foreman/create_order_update.html'
    ServiceFormSet = modelformset_factory(ServiceOrder, form=ForemanService, can_delete=True)
    ExtraFormSet = modelformset_factory(ExtraServiceOrder, form=ForemanExtraService, can_delete=True)

    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        service_formset = self.ServiceFormSet(queryset=order.service.all(), prefix='service')
        extra_formset = self.ExtraFormSet(queryset=order.extra_service.all(), prefix='extra')
        return render(request, self.template_name, {'service_form': service_formset, 'extra_service_form' : extra_formset})
    def post(self, request, *args, **kwargs):
        print('POST')
        print(request.POST)
        order = Order.objects.get(pk=kwargs['pk'])
        data = request.POST
        service_form = self.ServiceFormSet(request.POST)
        extra_form = self.ExtraFormSet(request.POST)
        # foreman_order = self.model.objects.create(order_id=order.id)
        if service_form.is_valid() and extra_form.is_valid():
            print('IF')
            services = service_form.save(commit=False)
            for service in services:
                print(service)
                # foreman_order.service.add(service)
            extra = extra_form.save(commit=False)
            for ex in extra:
                print(ex)
                # foreman_order.extra_service.add(ex)
            # foreman_order.save()
        return redirect('crmapp:foremanorder_create', 1)

    def get_success_url(self):
        return redirect('crmapp:foremanupdate_create')
