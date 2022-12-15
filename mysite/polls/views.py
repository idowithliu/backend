from django.shortcuts import render
from django.http import HttpResponse

from django.contrib.auth.models import User, Group
from rest_framework import viewsets
from rest_framework import permissions
from polls.serializers import QuestionSerializer
from .models import Question

class QuestionViewSet(viewsets.ModelViewSet):
    queryset = Question.objects.all().order_by('question_text')
    serializer_class = QuestionSerializer

# Create your views here.
def index(request):
    return HttpResponse("Hello, World! You are at the polls index.")
