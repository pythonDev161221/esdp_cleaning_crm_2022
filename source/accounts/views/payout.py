from django.views.generic import ListView, CreateView

from accounts.forms import PayoutForm
from accounts.models import Payout


class PayoutListView(ListView):
    model = Payout
    context_object_name = 'payouts'
    template_name = 'account/payout_list.html'
    ordering = ['-date_payout', ]


class PayoutCreateView(CreateView):
    model = Payout
    form_class = PayoutForm
    template_name = 'account/payout_add.html'

    def form_valid(self, form):
        form.instance.salary = form.instance.staff.balance
        if form.instance.salary == 0:
            return self.form_invalid(form)
        form.instance.staff.nullify_salary(form.instance.salary)
        return super().form_valid(form)

