import datetime

from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.views import View

from crmapp.forms import ServiceOrderForm
from crmapp.models import ForemanOrderUpdate, Order, ServiceOrder, ForemanReport


class ForemanOrderUpdateCreateView(View):
    model = ForemanOrderUpdate
    template_name = 'foreman/create_order_update.html'
    ServiceFormSet = modelformset_factory(ServiceOrder, form=ServiceOrderForm, can_delete=True)

    def get(self, request, *args, **kwargs):
        try:
            foreman_order = self.model.objects.get(order_id=kwargs['pk'])
            service_formset = self.ServiceFormSet(queryset=foreman_order.services.filter(service__is_extra=False))
            extra_formset = self.ServiceFormSet(queryset=foreman_order.services.filter(service__is_extra=True))
            return render(request, self.template_name,
                          {'service_form': service_formset, 'extra_service_form' : extra_formset})
        except:
            order = Order.objects.get(pk=kwargs['pk'])
            service_formset = self.ServiceFormSet(queryset=order.order_services.filter(service__is_extra=False))
            extra_formset = self.ServiceFormSet(queryset=order.order_services.filter(service__is_extra=True))
            return render(request, self.template_name,
                          {'service_form': service_formset, 'extra_service_form': extra_formset})

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        service_form = self.ServiceFormSet(request.POST, request.FILES)
        foreman_order, created = self.model.objects.get_or_create(order_id=order.pk)
        if service_form.is_valid():
            for form in service_form:
                if form.cleaned_data:
                    f = form.save()
                    foreman_order.services.add(f)
            service_form.save()
            foreman_order.save()
        return redirect('crmapp:foremanorder_create', order.id)


class InPlaceView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        staff = order.order_cliners.get(staff_id=request.user.id)
        if not staff.in_place:
            staff.in_place = datetime.datetime.now()
            staff.save()
        return redirect('crmapp:order_detail', kwargs['pk'])

class WorkStartView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        staff = order.order_cliners.get(staff_id=request.user.id)
        if staff.is_brigadier == True:
            order.foreman_order_report.start_at = datetime.datetime.now()
        if not staff.work_start:
            staff.work_start = datetime.datetime.now()
            staff.save()
        return redirect('crmapp:order_detail', kwargs['pk'])

class WorkEndView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        staff = order.order_cliners.get(staff_id=request.user.id)
        if staff.is_brigadier == True:
            foreman_report, created = ForemanReport.objects.get_or_create(order_id=order.pk)
            foreman_report.end_at = datetime.datetime.now()
            foreman_report.save()
        return redirect('crmapp:order_detail', kwargs['pk'])

