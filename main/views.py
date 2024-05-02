from django.shortcuts import render

# Create your views here.

from django.shortcuts import render
from django.http import HttpResponse

def home(request):

    return render(request, 'main/home.html')

def topic(request, topic_id):

    return render(request, 'topic/.html')