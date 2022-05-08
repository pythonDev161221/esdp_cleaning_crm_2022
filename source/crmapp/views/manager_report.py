from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.forms import modelformset_factory
from django.http import Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views.generic import ListView, FormView

from crmapp.forms import ManagerReportForm, BaseManagerReportFormSet
from crmapp.models import ManagerReport, Order

User = get_user_model()


class ManagerReportCreateView(FormView):
    model = ManagerReport
    form_class = ManagerReportForm
    template_name = 'manager_report/report_create.html'

    def get(self, request, *args, **kwargs):
        if self.model.objects.filter(order=self.kwargs['pk']):
            messages.warning(self.request, f'Менеджерский отчет уже существует!')
            return redirect("crmapp:order_detail", pk=self.kwargs['pk'])
        else:
            return super(ManagerReportCreateView, self).get(request, *args, **kwargs)

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        staff_and_salary = order.manager_report_salary_staffs()
        ManagerFormset = modelformset_factory(ManagerReport, form=ManagerReportForm, formset=BaseManagerReportFormSet, extra=order.cleaners.count())
        formset = ManagerFormset(prefix='extra', queryset=order.cleaners.all())
        staff_numeric_value = 0
        for forms in formset:
            forms.fields['cleaner'].queryset = order.cleaners.all()
            forms.initial = {"cleaner": staff_and_salary[staff_numeric_value][0],  "salary": round(staff_and_salary[staff_numeric_value][1], 0)}
            staff_numeric_value += 1
        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        ManagerFormset = modelformset_factory(ManagerReport, form=ManagerReportForm, extra=order.cleaners.count())
        formset = ManagerFormset(request.POST, request.FILES, prefix="extra")
        if formset.is_valid():
            salary_all_sum = [form.instance.salary for form in [fs for fs in formset.forms]]
            if sum(salary_all_sum) > order.get_total():  # Вместо order.get_total() указать поле зп выделенное для клинеров
                return render(self.request, self.template_name,
                              {"salary_errors": f"Сумма превышает общий допустимый лимит: {order.get_total()}",
                               "formset": formset})# Вместо order.get_total() указать поле зп выделенное для клинеров
            else:
                messages.success(self.request, f'Операция успешно выполнена!')
                return self.form_valid(formset)
        else:
            messages.warning(self.request, f'Операция не выполнена!')
            return self.form_invalid(formset)

    def form_valid(self, formset):
        with transaction.atomic():
            order = get_object_or_404(Order, pk=self.kwargs['pk'])
            forms = formset.save(commit=False)
            for form in forms:
                form.order = order
                form.cleaner.add_salary(form.get_salary())
                form.save()
        return redirect('crmapp:manager_report_list')

    def form_invalid(self, formset):
        context = self.get_context_data()
        context["formset"] = formset
        return render(self.request, self.template_name, context)


class ManagerReportListView(ListView):
    model = ManagerReport
    template_name = 'manager_report/report_list.html'
    context_object_name = 'manager_reports'







