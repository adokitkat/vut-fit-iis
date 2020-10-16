from django.shortcuts import render
from django.shortcuts import render

from .models import User
# Temporary view
from django.http import HttpResponse
def index(request):
    users = User.objects.all()
    context = {'Users': users}
    return render(request, 'landing_page/index.html', context)
