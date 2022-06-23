from rest_framework import serializers

from crmapp.models import Client, ServiceOrder, Service


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'phone', 'organization')
        read_only_fields = ('id',)


class OrderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        depth = 1
        fields = ['service', 'amount', 'rate']
        read_only_fields = ['id', 'order']


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name',)
        read_only_fields = ('id',)
