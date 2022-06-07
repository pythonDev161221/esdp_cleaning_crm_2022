from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db import transaction
from django.forms import modelformset_factory, HiddenInput
from django.shortcuts import get_object_or_404, redirect, render
from django.views.generic import ListView, FormView

from crmapp.forms import ManagerReportForm, BaseManagerReportFormSet
from crmapp.models import ManagerReport, Order, StaffOrder

from crmapp.forms import FilterForm

User = get_user_model()


class ManagerReportCreateView(FormView):
    model = ManagerReport
    form_class = ManagerReportForm
    template_name = 'manager_report/report_create.html'

    def get(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        if self.model.objects.filter(order=order):
            messages.warning(self.request, f'Менеджерский отчет уже существует!')
            return redirect("crmapp:order_detail", pk=self.kwargs['pk'])
        else:
            if order.manager_report_salary_staffs():
                return super().get(request, *args, **kwargs)
            else:
                messages.warning(self.request, f'Нельзя создать отчет, пока клинеры не принимут заказ!')
                return redirect("crmapp:order_detail", pk=self.kwargs['pk'])

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        staff_order = StaffOrder.objects.filter(order=order)
        context['staff_order'] = staff_order
        context['order'] = order
        staff_and_salary = order.manager_report_salary_staffs()
        ManagerFormset = modelformset_factory(ManagerReport, form=ManagerReportForm, formset=BaseManagerReportFormSet,
                                              extra=len(staff_and_salary))
        formset = ManagerFormset(prefix='extra',)
        staff_numeric_value = 0
        for forms in formset:
            if not staff_and_salary[staff_numeric_value][1] == None:
                forms.initial = {"cleaner": staff_and_salary[staff_numeric_value][0],
                                 "salary": round(staff_and_salary[staff_numeric_value][1], 0)}
            else:
                forms.fields.pop('bonus') and forms.fields.pop('bonus_description')
                forms.fields['salary'].widget = HiddenInput(attrs={"value": 0})
                forms.initial = {"cleaner": staff_and_salary[staff_numeric_value][0]}
            staff_numeric_value += 1
        context['formset'] = formset
        staff_order = StaffOrder.objects.filter(order=order)
        context['staff_order'] = staff_order
        context['order'] = order
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
                               "formset": formset})  # Вместо order.get_total() указать поле зп выделенное для клинеров
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
    filter_form_class = FilterForm

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value_first = self.get_search_value_first()
        self.search_value_last = self.get_search_value_last()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.search_value_first and self.search_value_last:
            queryset = queryset.filter(created_at__range=(self.search_value_first, self.search_value_last))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.filter_form_class()
        return context

    def get_form(self):
        return self.filter_form_class(self.request.GET)

    def get_search_value_first(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("start_date")

    def get_search_value_last(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("end_date")