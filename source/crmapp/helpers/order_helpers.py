from django.contrib.auth import get_user_model
from django.forms import inlineformset_factory
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views.generic import FormView

from crmapp.forms import ServiceOrderForm, OrderStaffForm
from crmapp.models import Order, ServiceOrder, StaffOrder

User = get_user_model()

ServiceFormset = inlineformset_factory(
    Order,
    ServiceOrder,
    form=ServiceOrderForm,
    exclude=['order'],
    extra=3,
    can_delete=False
)

StaffFormset = inlineformset_factory(
    Order,
    StaffOrder,
    form=OrderStaffForm,
    fields=['staff', 'is_brigadier'],
    extra=5,
    can_delete=False
)


class BaseOrderCreateView(FormView):
    template_name = None
    formset = None
    object = None
    form_helper = None
    formset_helper = None

    def get_context_data(self, **kwargs):
        kwargs['formset'] = self.formset()
        kwargs['form_helper'] = self.form_helper()
        kwargs['formset_helper'] = self.formset_helper()
        return super().get_context_data(**kwargs)

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        formset = self.formset(self.request.POST)
        if form.is_valid() and formset.is_valid():
            return self.form_valid(form, formset)
        else:
            return self.form_invalid(form, formset)

    def form_valid(self, form, formset=None):
        pass

    def form_invalid(self, form, formset=None):
        return self.render_to_response(
            self.get_context_data(
                form=form,
                formset=formset,
            )
        )


class ModalFormView(FormView):
    form_class = None

    def post(self, request, *args, **kwargs):
        form = self.form_class(self.request.POST)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        form.instance.order_id = self.kwargs.get('pk')
        form.save()
        return HttpResponseRedirect(self.get_success_url())

