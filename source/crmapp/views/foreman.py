from django.contrib.auth.mixins import PermissionRequiredMixin
from django.forms import modelformset_factory
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render, get_object_or_404
from django.urls import reverse
from django.views import View
from django.views.generic import FormView, DetailView, CreateView

from crmapp.forms import ServiceOrderForm, ForemanExpenseForm
from crmapp.models import ForemanOrderUpdate, Order, ServiceOrder, ForemanPhoto, ForemanExpenses, \
    StaffOrder

from tgbot.handlers.orders.tg_order_staff import manager_alert, manager_expense_alert


class ForemanOrderUpdateCreateView(PermissionRequiredMixin, FormView):
    model = ForemanOrderUpdate
    template_name = 'foreman/create_order_update.html'
    ServiceFormSet = modelformset_factory(ServiceOrder, form=ServiceOrderForm, can_delete=True)
    permission_required = "crmapp.change_foremanorderupdate"

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
                    foreman_order.services.add(f)
            service_form.save()
            foreman_order.save()
            manager_alert(order)
        return redirect('crmapp:order_detail', order.id)

    def has_permission(self):
        order = get_object_or_404(Order, pk=self.kwargs.get("pk"))
        if order.status == 'finished' or order.status == "canceled":
            return super().has_permission()
        return self.request.user == order.get_brigadier() and not order.get_brigadier().work_start


class ServiceForemanOrderCreateView(PermissionRequiredMixin, CreateView):
    model = ServiceOrder
    template_name = 'service_order/service_order_create.html'
    form_class = ServiceOrderForm
    permission_required = "crmapp.add_foremanorderupdate"

    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        foreman_order, created = ForemanOrderUpdate.objects.get_or_create(order_id=order.pk)
        self.object = form.save(commit=False)
        self.object.total = self.object.service_total()
        self.object.order = order
        self.object.save()
        manager_alert(order)
        messages.success(self.request, f'Вы успешно добавили услугу в заказ № {order.id}!')
        foreman_order.services.add(self.object)
        return HttpResponseRedirect(self.get_success_url())

    def get_success_url(self):
        return reverse('crmapp:order_detail', kwargs={'pk': self.object.order.pk})

    def has_permission(self):
        order = get_object_or_404(Order, pk=self.kwargs.get("pk"))
        if order.status == 'finished' or order.status == "canceled":
            return super().has_permission()
        return self.request.user == order.order_cleaners.get(is_brigadier=True).staff


class ForemanExpenseView(PermissionRequiredMixin, CreateView):
    model = ForemanExpenses
    form_class = ForemanExpenseForm
    template_name = 'foreman/expense.html'
    permission_required = "crmapp.add_foremanexpenses"

    def form_valid(self, form):
        order = get_object_or_404(Order, pk=self.kwargs.get('pk'))
        foreman_report = StaffOrder.objects.get(order_id=order.pk, is_brigadier=True)
        self.object = form.save(commit=False)
        self.object.foreman_report = foreman_report
        self.object.save()
        manager_expense_alert(order)
        messages.success(self.request, f'Вы успешно добавили услугу в заказ № {order.id}!')
        return redirect('crmapp:order_detail', order.pk)

    def has_permission(self):
        order = get_object_or_404(Order, pk=self.kwargs.get("pk"))
        if order.status == 'finished' or order.status == "canceled":
            return super().has_permission()
        return self.request.user == order.get_brigadier()


class PhotoBeforeView(PermissionRequiredMixin, View):
    permission_required = "crmapp.add_foremanphoto"

    def post(self, request, *args, **kwargs):
        photo_before = request.FILES.getlist('photo_before')
        photo_after = request.FILES.getlist('photo_after')
        foreman_report = StaffOrder.objects.get(order_id=self.kwargs.get("pk"), is_brigadier=True)
        foreman_report.save()
        for img in photo_before:
            if img.content_type == 'image/jpeg':
                foreman_photo = ForemanPhoto.objects.create(foreman_report=foreman_report)
                foreman_photo.image = img
                foreman_photo.is_after = False
                foreman_photo.save()
                messages.success(self.request, f'Вы добавили ФОТО ДО')
        for img in photo_after:
            if img.content_type == 'image/jpeg':
                foreman_photo = ForemanPhoto.objects.create(foreman_report=foreman_report)
                foreman_photo.image = img
                foreman_photo.is_after = True
                foreman_photo.save()
                messages.success(self.request, f'Вы добавили ФОТО ПОСЛЕ')
        return redirect('crmapp:order_detail', kwargs['pk'])

    def has_permission(self):
        order = get_object_or_404(Order, pk=self.kwargs.get("pk"))
        if order.status == 'finished' or order.status == "canceled":
            return super().has_permission()
        return self.request.user == order.order_cleaners.get(is_brigadier=True).staff


class PhotoDetailView(PermissionRequiredMixin, DetailView):
    model = Order
    template_name = 'foreman/photo_report.html'
    context_object_name = 'foreman_report'
    permission_required = "crmapp.view_foremanphoto"

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(**kwargs)
        order = StaffOrder.objects.get(order=self.get_object().pk, is_brigadier=True)
        foreman_photo = ForemanPhoto.objects.filter(foreman_report=order.pk)
        photos_before = [i for i in foreman_photo.filter(is_after=False)]
        photos_after = [i for i in foreman_photo.filter(is_after=True)]
        context['photos_before'] = photos_before
        context['photos_after'] = photos_after
        return context

    def has_permission(self):
        order = get_object_or_404(Order, pk=self.kwargs.get("pk"))
        return super().has_permission() or self.request.user == order.order_cleaners.get(is_brigadier=True).staff
