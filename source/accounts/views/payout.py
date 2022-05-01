from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView

from accounts.forms import PayoutForm
from accounts.models import Payout, Staff


class PayoutListView(ListView):
    model = Payout
    context_object_name = 'payouts'
    template_name = 'account/payout_list.html'
    ordering = ['-date_payout', ]


class PayoutCreateView(CreateView):
    model = Payout
    form_class = PayoutForm
    template_name = 'account/payout_add.html'
    success_url = reverse_lazy('accounts:staff-list')
    context_object_name = 'staff_payout'

    def post(self, request, *args, **kwargs):
        staff = get_object_or_404(Staff, pk=self.kwargs['pk'])
        if staff.balance > 0:
            Payout.objects.create(staff=staff, salary=staff.balance)
            staff.nullify_salary()
            messages.success(self.request, f'Баланс сотрудника {staff.first_name} {staff.last_name} успешно списан!')
        else:
            messages.warning(self.request, f'Баланс сотрудника {staff.first_name} {staff.last_name} составляет {staff.balance} cом! Операция невозможна! ')
        return HttpResponseRedirect(self.success_url)