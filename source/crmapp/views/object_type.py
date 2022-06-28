from django.contrib.auth.mixins import PermissionRequiredMixin
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView

from crmapp.models import ObjectType

from crmapp.forms import ObjectTypeForm


class ObjectTypeListView(PermissionRequiredMixin, ListView):
    model = ObjectType
    context_object_name = 'object_types'
    template_name = 'object_type/list.html'
    permission_required = "crmapp.view_objecttype"
    paginate_by = 10
    paginate_orphans = 0


class ObjectTypeCreateView(PermissionRequiredMixin, CreateView):
    model = ObjectType
    form_class = ObjectTypeForm
    template_name = 'object_type/create.html'
    success_url = reverse_lazy('crmapp:object_type_list')
    permission_required = "crmapp.add_objecttype"


class ObjectTypeUpdateView(PermissionRequiredMixin, UpdateView):
    model = ObjectType
    form_class = ObjectTypeForm
    template_name = 'object_type/update.html'
    permission_required = "crmapp.change_objecttype"


class ObjectTypeDeleteView(PermissionRequiredMixin, DeleteView):
    model = ObjectType
    context_object_name = 'object_type'
    template_name = "object_type/delete.html"
    permission_required = "crmapp.delete_objecttype"

    def get_success_url(self):
        return reverse_lazy("crmapp:object_type_list")
