from django.contrib.auth.mixins import PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, DeleteView, FormView

from crmapp.forms import InventoryForm, InventoryOrderForm, InventoryOrderFormSet
from crmapp.models import Inventory, InventoryOrder, Order

from crmapp.views.search_view import SearchView


class InventoryListView(PermissionRequiredMixin, SearchView):
    model = Inventory
    context_object_name = 'inventories'
    template_name = 'inventories/inventory_list.html'
    permission_required = "crmapp.view_inventory"
    search_fields = ["name__icontains", "description__icontains"]


class InventoryCreateView(PermissionRequiredMixin, CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventories/create.html'
    permission_required = "crmapp.add_inventory"


class InventoryUpdateView(PermissionRequiredMixin, UpdateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'inventories/update.html'
    permission_required = "crmapp.change_inventory"


class InventoryDeleteView(PermissionRequiredMixin, DeleteView):
    model = Inventory
    template_name = "inventories/delete.html"
    permission_required = "crmapp.delete_inventory"

    def get_success_url(self):
        return reverse_lazy("crmapp:inventory_index")


class InventoryOrderCreateView(PermissionRequiredMixin, FormView):
    model = InventoryOrder
    form_class = InventoryOrderForm
    template_name = "inventories/inventory_order_create.html"
    permission_required = "crmapp.add_inventoryorder"

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

    def has_permission(self):
        order = get_object_or_404(Order, pk=self.kwargs["pk"])
        return self.request.user == order.manager and super().has_permission() or self.request.user.is_staff


class InventoryOrderRemoveView(PermissionRequiredMixin, DeleteView):
    model = InventoryOrder
    template_name = "inventories/inventory_order_delete.html"
    context_object_name = "inventory_order"

    def get_success_url(self):
        return reverse_lazy("crmapp:order_detail", kwargs={"pk": self.object.order.pk})

    def has_permission(self):
        return self.request.user == self.get_object().order.manager or self.request.user.is_staff

