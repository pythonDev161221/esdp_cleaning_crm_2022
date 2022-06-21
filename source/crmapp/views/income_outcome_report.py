from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from crmapp.models import Order

from crmapp.forms import FilterForm


class IncomeOutcomeReportView(PermissionRequiredMixin, ListView):
    model = Order
    template_name = '../templates/income_outcome_report/income_outcome_report.html'
    context_object_name = 'orders'
    filter_form_class = FilterForm
    permission_required = "crmapp.сan_view_income_outcome_report"

    def get(self, request, *args, **kwargs):
        self.form = self.get_form()
        self.search_value_first = self.get_search_value_first()
        self.search_value_last = self.get_search_value_last()
        return super().get(request, *args, **kwargs)

    def get_queryset(self):
        queryset = Order.objects.order_by('work_start').exclude(is_deleted=True).exclude(
                status='new')
        if self.search_value_first and self.search_value_last:
            queryset = queryset.filter(work_start__range=(self.search_value_first, self.search_value_last))
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(object_list=object_list, **kwargs)
        context['form'] = self.filter_form_class()
        context["order_sum"] = 0
        context["cleaner_outcome"] = 0
        context["other_outcome"] = 0
        context["total"] = 0
        for order in self.get_queryset():
            context["order_sum"] += order.get_total()
            context["cleaner_outcome"] += order.get_all_staff_expenses()
            context["other_outcome"] += order.get_foreman_expenses()
            context["total"] += order.get_income_outcome()
        return context

    def get_form(self):
        return self.filter_form_class(self.request.GET)

    def get_search_value_first(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("start_date")

    def get_search_value_last(self):
        if self.form.is_valid():
            return self.form.cleaned_data.get("end_date")
