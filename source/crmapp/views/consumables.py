from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from crmapp.forms import InventoryForm, CleansearForm
from crmapp.models import Inventory, Cleansear


class InventoryListView(ListView):
    model = Inventory
    context_object_name = 'inventories'
    template_name = 'consumables/inventory_list.html'


class InventoryCreateView(CreateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'consumables/create.html'


class InventoryUpdateView(UpdateView):
    model = Inventory
    form_class = InventoryForm
    template_name = 'consumables/update.html'


class InventoryDeleteView(DeleteView):
    model = Inventory
    template_name = "consumables/delete.html"

    def get_success_url(self):
        return reverse("crmapp:inventory_index")




class CleansearListView(ListView):
    model = Cleansear
    context_object_name = 'cleansears'
    template_name = 'consumables/cleansear_list.html'


class CleansearCreateView(CreateView):
    model = Cleansear
    form_class = CleansearForm
    template_name = 'consumables/create.html'


class CleansearUpdateView(UpdateView):
    model = Cleansear
    form_class = CleansearForm
    template_name = 'consumables/update.html'


class CleansearDeleteView(DeleteView):
    model = Cleansear
    template_name = "consumables/delete.html"

    def get_success_url(self):
        return reverse("crmapp:cleansear_index")