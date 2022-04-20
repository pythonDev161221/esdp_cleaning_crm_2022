from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from crmapp.forms import InventoryForm
from crmapp.models import Inventory


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