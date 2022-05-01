from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.views import View

from crmapp.forms import ServiceOrderForm
from crmapp.models import ForemanOrderUpdate, Order, Service


class ForemanOrderUpdateCreateView(View):
    model = ForemanOrderUpdate
    template_name = 'foreman/create_order_update.html'
    ServiceFormSet = modelformset_factory(Service, form=ServiceOrderForm, can_delete=True)


    def get(self, request, *args, **kwargs):
        try:
            foreman_order =  self.model.objects.get(order_id=kwargs['pk'])
            service_formset = self.ServiceFormSet(queryset=foreman_order.service.filter(is_extra=False), prefix='service')
            extra_formset = self.ServiceFormSet(queryset=foreman_order.service.filter(is_extra=True), prefix='extra')
            return render(request, self.template_name,
                          {'service_form': service_formset, 'extra_service_form' : extra_formset})
        except:
            order = Order.objects.get(pk=kwargs['pk'])
            service_formset = self.ServiceFormSet(queryset=order.services.filter(is_extra=False), prefix='service')
            print(order.services.all())
            extra_formset = self.ServiceFormSet(queryset=order.services.filter(is_extra=True), prefix='extra')
            return render(request, self.template_name,
                          {'service_form': service_formset, 'extra_service_form': extra_formset})

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        service_form = self.ServiceFormSet(request.POST, request.FILES, prefix='service')
        foreman_order, created = self.model.objects.get_or_create(order_id=order.pk)
        if service_form.is_valid():
            for form in service_form:
                if form.cleaned_data:
                    f = form.save()
                    foreman_order.service.add(f)
            service_form.save()
            foreman_order.save()
        return redirect('crmapp:foremanorder_create', order.id)
