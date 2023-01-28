from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .emails.main import EmailClient
from django.shortcuts import render
from django.http import HttpResponse
from django.core.exceptions import ValidationError
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.hashers import check_password

# from rest_framework.authentication.BaseAuthentication import authenticate
# from authentication_django_rest_framework.apps.core.api.authentication.authentications import JWTAccessTokenAuthentication
# from rest_framework_jwt.serializers import VerifyJSONWebTokenSerializer
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
        print(guest["is_attending"])
        guest_obj.dietary_restrictions = guest['dietary_restrictions'] if guest_obj.is_attending else ""
        guest_obj.save()

    invite.finished = True
    invite.save()
    response = {"status": "ok",
                "message": "your RSVP was successfully saved!"}
    return HttpResponse(json.dumps(response), content_type="application/json", status=200)


@csrf_exempt
def send_emails(request):
    if request.method != "POST":
        response = {"status": "error", "message": "Method not allowed"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=405)

    body_unicode = request.body.decode('utf-8')
    body = json.loads(body_unicode)

    if not "username" in body or not "password" in body:
        response = {"status": "error",
                    "message": "Username or password was not provided"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)

    user = User.objects.filter(username=body['username']).first()

    if not user:
        response = {"status": "error",
                    "message": "a user with this username was not found"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=404)

    if not user.check_password(body['password']):
        response = {"status": "error",
                    "message": "the password provided was not correct"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=401)

    if not user.has_perms(["superuser"]):
        response = {"status": "error",
                    "message": "the user does not have superuser permissions"}
        return HttpResponse(json.dumps(response), content_type="application/json", status=401)

    if not "email_content" in body:
        response = {"status": "error",
                    "message": "an email body was not provided as \"email_content\""}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)

    if not "subject" in body:
        response = {"status": "error",
                    "message": "an email subject was not provided as \"subject\""}
        return HttpResponse(json.dumps(response), content_type="application/json", status=400)

    content: str = body['email_content']

    all_emails = "all_emails" in body and body['all_emails'] == True

    invites = Invite.objects.all()
    if not all_emails:
        invites = invites.filter(finished=False)

    client = EmailClient()
    for invite in invites:
        client.send_email(
            invite.email, body['subject'], content.format(**invite.__dict__))

    response = {"status": "ok",
                "message": f"Successfully sent {invites.__len__()} emails!"}
    return HttpResponse(json.dumps(response), content_type="application/json", status=200)
