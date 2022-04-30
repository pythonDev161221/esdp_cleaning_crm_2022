from django.contrib.auth import get_user_model
from django.forms import modelformset_factory
from django.shortcuts import get_object_or_404, redirect
from django.views.generic import CreateView, ListView

from crmapp.forms import ManagerReportForm, BaseManagerReportFormSet
from crmapp.models import ManagerReport, Order

User = get_user_model()


class ManagerReportCreateView(CreateView):
    model = ManagerReport
    form_class = ManagerReportForm
    template_name = 'manager_report/report_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        cleaners = User.objects.filter(orders=order)
        ManagerFormset = modelformset_factory(ManagerReport, form=ManagerReportForm, formset=BaseManagerReportFormSet, extra=cleaners.count())
        formset = ManagerFormset(prefix='extra', queryset=cleaners)
        for forms in formset:
            forms.fields['cleaner'].queryset = cleaners

        context['formset'] = formset
        return context

    def post(self, request, *args, **kwargs):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        cleaners = User.objects.filter(orders=order)
        ManagerFormset = modelformset_factory(ManagerReport, form=ManagerReportForm, extra=cleaners.count())
        formset = ManagerFormset(request.POST, request.FILES, prefix="extra")
        if formset.is_valid():
            return self.form_valid(formset)

    def form_valid(self, formset):
        order = get_object_or_404(Order, pk=self.kwargs['pk'])
        datas = formset.save(commit=False)
        for data in datas:
            data.order = order
            data.save()
        return redirect('crmapp:manager_report_list')


class ManagerReportListView(ListView):
    model = ManagerReport
    template_name = 'manager_report/report_list.html'
    context_object_name = 'manager_reports'







