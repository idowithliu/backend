from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from registry.serializers import RegistrySerializer
from .models import RegistryItem

class RegistryViewSet(viewsets.ModelViewSet):
    queryset = RegistryItem.objects.all().order_by('name')
    serializer_class = RegistrySerializer
