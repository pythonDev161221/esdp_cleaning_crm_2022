from rest_framework import serializers

from crmapp.models import Client, Fine, Bonus, Inventory, ObjectType, ServiceOrder, Service, InventoryOrder, Order


class OrderListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ('work_start', "id", "address", "status",)


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'phone', 'organization')


class OrderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        depth = 1
        fields = ['service', 'amount', 'rate']


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name', 'unit', 'price', 'is_extra')


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = ('id', 'category', 'fine', 'criteria', 'value', 'description')


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = ('id', 'bonus', 'value')


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'name', 'description')


class ObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectType
        fields = ('id', 'name')


class InventoryOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = InventoryOrder
        fields = ('id', 'inventory', 'amount')
