from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from rsvp.serializers import InviteSerializer
from .models import Invite

class InviteViewSet(viewsets.ModelViewSet):
    queryset = Invite.objects.all().order_by('family_name')
    serializer_class = InviteSerializer
