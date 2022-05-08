import datetime

from django.forms import modelformset_factory
from django.shortcuts import redirect, render
from django.views import View
from django.views.generic import FormView, DetailView

from crmapp.forms import ServiceOrderForm
from crmapp.models import ForemanOrderUpdate, Order, ServiceOrder, ForemanReport, ForemanPhoto


class ForemanOrderUpdateCreateView(FormView):
    model = ForemanOrderUpdate
    template_name = 'foreman/create_order_update.html'
    ServiceFormSet = modelformset_factory(ServiceOrder, form=ServiceOrderForm, can_delete=True)

    def get(self, request, *args, **kwargs):
        try:
            foreman_order = self.model.objects.get(order_id=kwargs['pk'])
            service_formset = self.ServiceFormSet(queryset=foreman_order.services.all())
            return render(request, self.template_name,
                          {'service_form': service_formset})
        except:
            order = Order.objects.get(pk=kwargs['pk'])
            service_formset = self.ServiceFormSet(queryset=order.order_services.all())
            return render(request, self.template_name,
                          {'service_form': service_formset})

    def post(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        service_form = self.ServiceFormSet(request.POST, request.FILES)
        foreman_order, created = self.model.objects.get_or_create(order_id=order.pk)
        if service_form.is_valid():
            for form in service_form:
                if form.cleaned_data:
                    f = form.save()
                    print(f'f = {f}')
                    foreman_order.services.add(f)
            service_form.save()
            foreman_order.save()
        return redirect('crmapp:foremanorder_create', order.id)


class InPlaceView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        staff = order.order_cliners.get(staff_id=request.user.id)
        if staff.is_brigadier == True:
            ForemanReport.objects.create(order_id=kwargs['pk'])
        if not staff.in_place:
            staff.in_place = datetime.datetime.now()
            staff.save()
        return redirect('crmapp:order_detail', kwargs['pk'])

class WorkStartView(View):
    def get(self, request, *args, **kwargs):
        order = Order.objects.get(pk=kwargs['pk'])
        staff = order.order_cliners.get(staff_id=request.user.id)
        foreman_report, created = ForemanReport.objects.get(order_id=kwargs['pk'])
        if staff.is_brigadier == True:
            foreman_report.start_at = datetime.datetime.now()
            foreman_report.save()
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


class PhotoBeforeView(View):
    def post(self, request, *args, **kwargs):
        photo_before = request.FILES.getlist('photo_before')
        photo_after = request.FILES.getlist('photo_after')
        foreman_report, created = ForemanReport.objects.get_or_create(order_id=kwargs['pk'])
        foreman_report.save()
        for img in photo_before:
            print(f'img = {img}')
            if img.content_type == 'image/jpeg':
                foreman_photo = ForemanPhoto.objects.create()
                foreman_photo.image = img
                foreman_photo.is_after = False
                foreman_photo.foreman_report = foreman_report
                foreman_photo.save()
        for img in photo_after:
            print(f'img = {img}')
            if img.content_type == 'image/jpeg':
                foreman_photo = ForemanPhoto.objects.create()
                foreman_photo.image = img
                foreman_photo.is_after = True
                foreman_photo.foreman_report = foreman_report
                foreman_photo.save()
        return redirect('crmapp:order_detail', kwargs['pk'])


class PhotoDetailView(DetailView):
    model = Order
    template_name = 'foreman/photo_report.html'
    context_object_name = 'foreman_report'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        reports = self.object.foreman_order_report.all()
        for ph in reports:
            context['photos_after'] = ph.foreman_photo.filter(is_after=True)
            context['photos_before'] = ph.foreman_photo.filter(is_after=False)
        return context