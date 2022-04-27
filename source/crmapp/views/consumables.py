from django.urls import reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from crmapp.forms import InventoryForm, CleanserForm
from crmapp.models import Inventory, Cleanser


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


class CleanserListView(ListView):
    model = Cleanser
    context_object_name = 'cleansers'
    template_name = 'consumables/cleanser_list.html'


class CleanserCreateView(CreateView):
    model = Cleanser
    form_class = CleanserForm
    template_name = 'consumables/create.html'


class CleanserUpdateView(UpdateView):
    model = Cleanser
    form_class = CleanserForm
    template_name = 'consumables/update.html'


class CleanserDeleteView(DeleteView):
    model = Cleanser
    template_name = "consumables/delete.html"

    def get_success_url(self):
        return reverse("crmapp:cleanser_index")