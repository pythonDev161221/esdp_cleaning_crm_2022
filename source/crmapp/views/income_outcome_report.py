from django.views.generic import ListView

from crmapp.models import Order


class IncomeOutcomeReportView(ListView):
    model = Order
    template_name = 'income_outcome_report/income_outcome_report.html'
    context_object_name = 'orders'
