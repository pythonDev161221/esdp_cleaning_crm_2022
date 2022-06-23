from rest_framework import serializers

from crmapp.models import Fine, Bonus, Inventory, ObjectType


class FineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fine
        fields = ('id', 'category', 'fine', 'criteria', 'value', 'description')
        read_only_fields = ('id',)


class BonusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bonus
        fields = ('id', 'bonus', 'value')
        read_only_fields = ('id',)


class InventorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Inventory
        fields = ('id', 'name', 'description')
        read_only_fields = ('id',)


class ObjectTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ObjectType
        fields = ('id', 'name')
        read_only_fields = ('id',)