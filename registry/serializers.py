from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Registry, RegistryItem

class RegistryItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = RegistryItem
        fields = ['name', 'id', 'price', 'picture', 'claimer']

class RegistrySerializer(serializers.HyperlinkedModelSerializer):
    registry_items = RegistryItemSerializer(many=True, read_only=True)
    class Meta:
        model = Registry
        fields = ('name', 'registry_items',)