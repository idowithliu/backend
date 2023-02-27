from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Registry, RegistryItem, Fund, Invite


class ClaimerIDSerializer(serializers.ModelSerializer):
    class Meta:
        model = Invite
        fields = ['pseudo_id']


class RegistryItemSerializer(serializers.ModelSerializer):
    claimer = ClaimerIDSerializer()

    class Meta:
        model = RegistryItem
        fields = ['name', 'url', 'photo_url', 'id', 'price', 'claimer']


class RegistrySerializer(serializers.HyperlinkedModelSerializer):
    registry_items = RegistryItemSerializer(many=True, read_only=True)

    class Meta:
        model = Registry
        fields = ('name', 'registry_items',)


class FundSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fund
        fields = ['id', 'name', 'total_amount_raised',
                  'goal', 'background_photo']
