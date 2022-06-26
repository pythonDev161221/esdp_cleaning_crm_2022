import django_filters

from crmapp.models import Order


class OrderFilter(django_filters.FilterSet):
    month = django_filters.NumberFilter(field_name='work_start', lookup_expr='month')
    year = django_filters.NumberFilter(field_name='work_start', lookup_expr='year')

    class Meta:
        model = Order
        fields = ['work_start', 'month', 'year']