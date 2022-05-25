from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, FormView

from crmapp.forms import InventoryForm, InventoryOrderForm, InventoryOrderFormSet
from crmapp.models import Inventory, InventoryOrder, Order


class InventoryListView(ListView):
    model = Inventory
    context_object_name = 'inventories'
    template_name = 'inventories/inventory_list.html'


class InventoryCreateView(CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventories/create.html'


class InventoryUpdateView(UpdateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventories/update.html'


class InventoryDeleteView(DeleteView):
    model = Inventory
    template_name = "inventories/delete.html"

    def get_success_url(self):
        return reverse("crmapp:inventory_index")


class InventoryOrderCreateView(FormView):
    model = InventoryOrder
    form_class = InventoryOrderForm
    template_name = "inventories/inventory_order_create.html"

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        context["formset"] = InventoryOrderFormSet(queryset=order.order_inventories.all())
        return context

    def post(self, request, *args, **kwargs):
        formset = InventoryOrderFormSet(request.POST)
        if formset.is_valid():
            return self.form_valid(formset)
        else:
            return self.form_invalid(formset)

    def form_valid(self, formset):
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        form = formset.save(commit=False)
        for fs in form:
            fs.order = order
            fs.save()
        return redirect("crmapp:order_detail", pk=order.pk)


class InventoryOrderRemoveView(DeleteView):
    model = InventoryOrder
    template_name = "inventories/inventory_order_delete.html"
    context_object_name = "inventory_order"

    def get_success_url(self):
        return reverse("crmapp:order_detail", kwargs={"pk": self.object.order.pk})
