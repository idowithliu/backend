from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from rsvp.serializers import InviteSerializer
from .models import Invite, Guest


class InviteViewSet(mixins.RetrieveModelMixin, viewsets.GenericViewSet):
    queryset = Invite.objects.all().order_by('family_name')
    serializer_class = InviteSerializer


@csrf_exempt
def submit_rsvp(request):
    raise Exception()
    if request.method != "POST":
        response = {"status": "error", "message": "Method not allowed"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if not "uuid" in body or not body['uuid']:
        response = {"status": "error",
                    "message": "an invite UUID was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    try:
        invite = Invite.objects.filter(uuid=body['uuid']).first()
    except ValidationError:
        response = {"status": "error",
                    "message": "the UUID provided is not valid"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)

    if not invite:
        response = {"status": "error",
                    "message": "an invite with the provided UUID was not found"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=404)

    if not "guests" in body or len(body['guests']) != len(invite.guests.all()):
        response = {"status": "error",
                    "message": "the guests array was not provided or is invalid"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)

    guests = body['guests']
    for guest in guests:
        guest_obj = Guest.objects.filter(id=guest['id']).first()
        if not guest_obj:
            response = {"status": "error",
                        "message": f"the guest with ID {guest['id']} was not found."}
            return HttpResponse(json.dumps(response), content_type="application/json", status=404)
        guest_obj.is_attending = guest['is_attending']
        guest_obj.dietary_restrictions = guest['dietary_restrictions'] if guest_obj.is_attending else ""
        guest_obj.save()

    invite.finished = True
    invite.save()
    response = {"status": "ok",
                "message": "your RSVP was successfully saved!"}
    return HttpResponse(json.dumps(response), content_type="application/json", status=200)
