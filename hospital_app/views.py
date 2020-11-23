from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect

from django.contrib.auth.decorators import login_required, permission_required

from .forms import CustomUserCreationForm
from .models import CustomUser

# Temporary view
from django.http import HttpResponse
#@login_required
#@permission_required('permission', raise_exception=True)
def index(request):
    users = CustomUser.objects.all()
    context = {'Users': users}
    return render(request, 'hospital_app/index.html', context)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            #username = form.cleaned_data.get('username')
            #raw_password = form.cleaned_data.get('password1')
            #user = authenticate(username=username, password=raw_password)
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'hospital_app/signup.html', {'form': form})