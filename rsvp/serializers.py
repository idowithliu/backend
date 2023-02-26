from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Invite, Guest
from registry.models import FundContrib


class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['name', 'id', 'dietary_restrictions', 'is_attending']


class FundContribSerializer(serializers.ModelSerializer):
    class Meta:
        model = FundContrib
        fields = []


class InviteSerializer(serializers.HyperlinkedModelSerializer):
    guests = GuestSerializer(many=True, read_only=True)
    fund_contribs = FundContribSerializer()

    class Meta:
        model = Invite
        fields = ('family_name', 'guests', 'uuid', 'pseudo_id',
                  'finished', 'fund_contribs',)
