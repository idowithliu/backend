from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
import json

from django.contrib.auth.models import User, Group
from rest_framework import viewsets, mixins
from registry.serializers import RegistrySerializer, FundSerializer
from .models import Registry, RegistryItem, Fund, FundContrib
from rsvp.models import Invite, Guest


class RegistryViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Registry.objects.filter(visible=True).order_by('name')
    serializer_class = RegistrySerializer


class FundViewSet(mixins.ListModelMixin, viewsets.GenericViewSet):
    queryset = Fund.objects.order_by('name')
    serializer_class = FundSerializer


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
    # if not "claimer_id" in body or not body['claimer_id']:
    #     response = {"status": "error",
    #                 "message": "a claimer ID was not provided"}
    #     return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    registry_item = RegistryItem.objects.filter(id=body['id']).first()
    if not registry_item or not registry_item.registry.visible:
        response = {"status": "error",
                    "message": "a registry item with this ID was not found"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=404)

    new_claimer = Invite.objects.filter(uuid=body['uuid']).first()
    if not new_claimer:
        response = {"status": "error",
                    "message": f"an invite with ID {body['claimer_id']} was not found"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=404)

    if (not registry_item.claimer_id is None) and new_claimer.invite.uuid != body['uuid']:
        response = {"status": "error",
                    "message": "this registry item has already been claimed by another party"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)

    registry_item.claimer = new_claimer
    registry_item.save()
    response = {"status": "ok",
                "message": "Thanks for claiming the registry item!"}
    return HttpResponse(json.dumps(response), content_type="application/json", status=200)


@csrf_exempt
def get_contribution_amount(request):
    if request.method != "POST":
        response = {"status": "error", "message": "Method not allowed"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if not "uuid" in body or not body['uuid']:
        response = {"status": "error",
                    "message": "an invite UUID was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    invite = Invite.objects.filter(uuid=body['uuid']).first()
    if not invite:
        response = {"status": "error",
                    "message": f"an invite with ID {body['uuid']} was not found"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=404)
    if not "id" in body or not body['id']:
        response = {"status": "error",
                    "message": "a fund ID was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    fund = Fund.objects.filter(id=body['id']).first()
    if not fund:
        response = {"status": "error",
                    "message": "a fund with this ID was not found"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=404)

    existing = FundContrib.objects.filter(
        contributer=invite, fund=fund).first()
    amount = existing.amount if existing else 0

    response = {"status": "ok",
                "amount": amount}
    return HttpResponse(json.dumps(response), content_type="application/json", status=200)


@csrf_exempt
def contribute(request):
    if request.method != "POST":
        response = {"status": "error", "message": "Method not allowed"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)
    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)
    if not "uuid" in body or not body['uuid']:
        response = {"status": "error",
                    "message": "an invite UUID was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    invite = Invite.objects.filter(uuid=body['uuid']).first()
    if not invite:
        response = {"status": "error",
                    "message": "an invite with this UUID was not found"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=404)
    if not "id" in body or not body['id']:
        response = {"status": "error",
                    "message": "a fund ID was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    if not "amount" in body or not body['amount']:
        response = {"status": "error",
                    "message": "a contribution amount was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    if body['amount'] <= 0:
        response = {"status": "error",
                    "message": "please enter a positive contribution amount"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)
    fund = Fund.objects.filter(id=body['id']).first()
    if not fund:
        response = {"status": "error",
                    "message": "a fund with this ID was not found"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=404)

    existing = FundContrib.objects.filter(
        contributer=invite, fund=fund).first()
    if existing and existing.amount > 0:
        response = {"status": "error",
                    "message": "you have already contributed to this fund!"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)

    new_contribution = FundContrib(
        contributer=invite, fund=fund, amount=body['amount'])
    new_contribution.save()

    response = {"status": "ok",
                "message": "Thanks for your donation!"}
    return HttpResponse(json.dumps(response), content_type="application/json", status=200)
