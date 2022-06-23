from rest_framework import serializers

from crmapp.models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = ('id', 'first_name', 'last_name', 'phone', 'organization')
        read_only_fields = ('id',)
