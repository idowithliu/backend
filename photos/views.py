from django.shortcuts import render

from rest_framework import viewsets, mixins
from photos.serializers import PhotoSerializer

from .models import Photo

# Create your views here.

class PhotoViewSet(mixins.ListModelMixin, mixins.RetrieveModelMixin, mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Photo.objects.all().order_by('id')
    serializer_class = PhotoSerializer