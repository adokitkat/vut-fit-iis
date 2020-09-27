from django.shortcuts import render

# Temporary view
from django.http import HttpResponse
def index(request):
    return HttpResponse("Hello, world. You're at your profile.")