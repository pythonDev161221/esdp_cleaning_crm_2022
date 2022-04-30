from django.db import transaction
from django.views.generic import ListView, DetailView, FormView, CreateView

from crmapp.forms import OrderForm, ServiceOrderFormSet
from crmapp.models import Order


class OrderListView(ListView):
    model = Order
    template_name = 'order/order_list.html'
    context_object_name = 'orders'


class OrderDetailView(DetailView):
    model = Order
    template_name = 'order/order_detail.html'
    context_object_name = 'order'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['extra_service'] = self.object.services.filter(is_extra=True)
        context['service'] = self.object.services.filter(is_extra=False)
        return context


class OrderCreateView(CreateView):
    model = Order
    form_class = OrderForm
    template_name = 'order/order_create.html'
    success_url = 'crmapp:order_index'

    def get_context_data(self, **kwargs):
        context = super(OrderCreateView, self).get_context_data(**kwargs)
        context['services'] = ServiceOrderFormSet()
        return context

    def post(self, request, *args, **kwargs):
        print(request.POST)

    def form_valid(self, form):
        context = self.get_context_data()
        services = context['services']
        print(services)
        with transaction.atomic():
            form.instance.manager = self.request.user
            self.object = form.save_m2m()
            if services.is_valid():
                services.instance = self.object
                services.save()
        return super(OrderCreateView, self).form_valid(form)


# class CollectionCreate(CreateView):
#     model = Collection
#     template_name = 'mycollections/collection_create.html'
#     form_class = CollectionForm
#     success_url = None
#
#     def get_context_data(self, **kwargs):
#         data = super(CollectionCreate, self).get_context_data(**kwargs)
#         if self.request.POST:
#             data['titles'] = CollectionTitleFormSet(self.request.POST)
#         else:
#             data['titles'] = CollectionTitleFormSet()
#         return data
#
#     def form_valid(self, form):
#         context = self.get_context_data()
#         titles = context['titles']
#         with transaction.atomic():
#             form.instance.created_by = self.request.user
#             self.object = form.save()
#             if titles.is_valid():
#                 titles.instance = self.object
#                 titles.save()
#         return super(CollectionCreate, self).form_valid(form)
#
#     def get_success_url(self):
#         return reverse_lazy('mycollections:collection_detail', kwargs={'pk': self.object.pk})

