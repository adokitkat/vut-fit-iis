from django.shortcuts import render
from django.shortcuts import render

from django.contrib.auth.decorators import login_required

from .models import User
# Temporary view
from django.http import HttpResponse
def index(request):
    users = User.objects.all()
    context = {'Users': users}
    return render(request, 'hospital_app/index.html', context)
