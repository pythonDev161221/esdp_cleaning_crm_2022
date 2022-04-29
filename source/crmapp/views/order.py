from django.views.generic import ListView, DetailView

from crmapp.models import Order, Service


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
