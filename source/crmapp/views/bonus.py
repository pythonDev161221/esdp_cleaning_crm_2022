
from django.contrib.auth.mixins import PermissionRequiredMixin

from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from crmapp.models import Bonus

from crmapp.forms import BonusForm


class BonusListView(PermissionRequiredMixin, ListView):
    model = Bonus
    context_object_name = 'bonuses'
    template_name = 'bonus/list.html'
    permission_required = "crmapp.view_bonus"


class BonusCreateView(PermissionRequiredMixin, CreateView):
    model = Bonus
    form_class = BonusForm
    template_name = 'bonus/create.html'
    permission_required = "crmapp.add_bonus"


class BonusUpdateView(PermissionRequiredMixin, UpdateView):
    model = Bonus
    form_class = BonusForm
    template_name = 'bonus/update.html'
    permission_required = "crmapp.change_bonus"


class BonusDeleteView(PermissionRequiredMixin, DeleteView):
    model = Bonus
    context_object_name = 'bonus'
    template_name = "bonus/delete.html"
    permission_required = "crmapp.delete_bonus"

    def get_success_url(self):
        return reverse_lazy("crmapp:bonus_list")
