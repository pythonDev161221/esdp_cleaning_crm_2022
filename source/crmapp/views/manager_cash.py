from django.contrib.auth.mixins import PermissionRequiredMixin
from django.views.generic import ListView

from crmapp.models import CashManager


class ManagerCashList(PermissionRequiredMixin, ListView):
    model = CashManager
    template_name = 'manager_cash/manager_cash_list.html'
    context_object_name = 'orders'
    permission_required = "crmapp.add_cashmanager"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["manager_cash"] = CashManager.objects.filter(is_nullify=True)
        return context

    def has_permission(self):
        return self.request.user.is_staff
