from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.views import View

from crmapp.forms import ForemanService, ForemanExtraService
from crmapp.models import ForemanOrderUpdate, Order, ServiceOrder, ExtraServiceOrder


class ForemanOrderUpdateCreateView(View):
    model = ForemanOrderUpdate
    template_name = 'foreman/create_order_update.html'
    ServiceFormSet = modelformset_factory(ServiceOrder, form=ForemanService, can_delete=True,)
    ExtraFormSet = modelformset_factory(ExtraServiceOrder, form=ForemanExtraService, can_delete=True)

    def get(self, request, *args, **kwargs):
        try:
            foreman_order =  self.model.objects.get(order_id=kwargs['pk'])
            service_formset = self.ServiceFormSet(queryset=foreman_order.service.all(), prefix='service')
            extra_formset = self.ExtraFormSet(queryset=foreman_order.extra_service.all(), prefix='extra')
            return render(request, self.template_name,
                          {'service_form': service_formset, 'extra_service_form': extra_formset})
        except:
            order = Order.objects.get(pk=kwargs['pk'])
            service_formset = self.ServiceFormSet(queryset=order.service.all(), prefix='service')
            extra_formset = self.ExtraFormSet(queryset=order.extra_service.all(), prefix='extra')
            return render(request, self.template_name,
                          {'service_form': service_formset, 'extra_service_form' : extra_formset})

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        service_form = self.ServiceFormSet(request.POST, request.FILES, prefix='service')
        extra_form = self.ExtraFormSet(request.POST, request.FILES, prefix='extra')
        foreman_order, created = self.model.objects.get_or_create(order_id=order.pk)
        if service_form.is_valid() and extra_form.is_valid():
            for form in service_form:
                if form.cleaned_data:
                    f = form.save()
                    foreman_order.service.add(f)
            for form in extra_form:
                if form.cleaned_data:
                    f = form.save()
                    foreman_order.extra_service.add(f)
            service_form.save()
            extra_form.save()
            foreman_order.save()
        return redirect('crmapp:foremanorder_create', 1)

