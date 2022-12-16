from django.contrib.auth.models import User, Group
from rest_framework import serializers

from .models import Invite, Guest

class GuestSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guest
        fields = ['name', 'dietary_restrictions']

class InviteSerializer(serializers.HyperlinkedModelSerializer):
    guests = GuestSerializer(many=True, read_only=True)
    class Meta:
        model = Invite
        fields = ('family_name', 'guests',)
