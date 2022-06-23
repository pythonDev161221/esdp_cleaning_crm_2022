from rest_framework import serializers

from crmapp.models import Client, Fine, Bonus, Inventory, ObjectType, ServiceOrder, Service


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'phone', 'organization')


class OrderServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = ServiceOrder
        depth = 1
        fields = ['service', 'amount', 'rate']


class ServiceListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = ('id', 'name',)
        read_only_fields = ('id',)


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

