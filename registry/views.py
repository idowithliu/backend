from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from registry.serializers import RegistrySerializer
from .models import Registry, RegistryItem
from rsvp.models import Guest


class RegistryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Registry.objects.filter(visible=True).order_by('name')
    serializer_class = RegistrySerializer


@csrf_exempt
def claim(request):
    if request.method != "POST":
        response = {"status": "error", "message": "Method not allowed"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if not "uuid" in body or not body['uuid']:
        response = {"status": "error",
                    "message": "an invite UUID was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    if not "id" in body or not body['id']:
        response = {"status": "error",
                    "message": "a registry item ID was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    if not "claimer_id" in body or not body['claimer_id']:
        response = {"status": "error",
                    "message": "a claimer ID was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    registry_item = RegistryItem.objects.filter(id=body['id']).first()
    if not registry_item or not registry_item.registry.visible:
        response = {"status": "error",
                    "message": "a registry item with this ID was not found"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=404)

    new_claimer = Guest.objects.filter(id=body['claimer_id']).first()
    if not new_claimer:
        response = {"status": "error",
                    "message": f"a guest with ID {body['claimer_id']} was not found"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=404)

    if (not registry_item.claimer_id is None) and new_claimer.invite.uuid != body['uuid']:
        response = {"status": "error",
                    "message": "this registry item has already been claimed by another person"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)

    registry_item.claimer_id = body['claimer_id']
    registry_item.claimer = new_claimer.name
    registry_item.save()
    response = {"status": "ok",
                "message": "the registry item was successfully claimed!"}
    return HttpResponse(json.dumps(response), content_type="application/json", status=200)
