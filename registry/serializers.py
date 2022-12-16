from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import RegistryItem

class RegistrySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = RegistryItem
        fields = ('name', 'price')