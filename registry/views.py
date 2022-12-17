from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from registry.serializers import RegistrySerializer
from .models import Registry, RegistryItem

class RegistryViewSet(viewsets.ModelViewSet):
    queryset = Registry.objects.filter(visible = True).order_by('name')
    serializer_class = RegistrySerializer


@csrf_exempt
def claim(request):
    if request.method != "POST":
        response = {"status": "error", "message": "Method not allowed"}
        return HttpResponse(json.dumps(response), content_type="application/json", status = 405)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if not "id" in body or not body['id']:
        response = {"status": "error", "message": "a registry item ID was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status = 400)
    if not "claimer" in body or not body['claimer']:
        response = {"status": "error", "message": "a claimer name was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status = 400)
    registry_item = RegistryItem.objects.filter(id=body['id']).first()
    if not registry_item or not registry_item.registry.visible:
        response = {"status": "error", "message": "a registry item with this ID was not found"}
        return HttpResponse(json.dumps(response), content_type="application/json", status = 404)
    if registry_item.claimer:
        response = {"status": "error", "message": "this registry item has already been claimed"}
        return HttpResponse(json.dumps(response), content_type="application/json", status = 400)

    registry_item.claimer = body['claimer']
    registry_item.save()
    response = {"status": "ok", "message": "the registry item was successfully claimed!"}
    return HttpResponse(json.dumps(response), content_type="application/json", status = 200)