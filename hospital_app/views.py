from django.contrib.auth import authenticate, login
from django.shortcuts import render

from django.contrib.auth.decorators import login_required, permission_required

from .models import CustomUser
# Temporary view
from django.http import HttpResponse
#@login_required
#@permission_required('permission', raise_exception=True)
def index(request):
    users = CustomUser.objects.all()
    context = {'Users': users}
    return render(request, 'hospital_app/index.html', context)
