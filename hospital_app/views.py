from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.core import serializers

from django.contrib.auth.decorators import login_required, permission_required

from .forms import CustomUserCreationForm, UserFilterForm
from .models import CustomUser

from django.views.generic import ListView

# Temporary view
from django.http import HttpResponse
#@login_required
#@permission_required('permission', raise_exception=True)

@login_required
def index(request):
    users = CustomUser.objects.all()
    context = {
        'Users': users,
        'index_active': True,
        }
    return render(request, 'hospital_app/index.html', context)
"""
class UpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Update
        fields = ("user", "content", "schedule", "image")

"""

class UsersView(ListView):
    model = CustomUser
    template_name = 'hospital_app/users.html'

    def get_queryset(self):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')
        
        if filter_field is None or filter_field == 'all':
            result_filter_field = CustomUser.objects.all()
        else: 
            result_filter_field = CustomUser.objects.filter(role=filter_field)
        
        if query is None or query == "":
            result = result_filter_field
        else:  
            if query.isdigit():
                result = result_filter_field.filter(pk=query)
            else:
                result = result_filter_field.filter(first_name__unaccent__icontains=query)
                result |= result_filter_field.filter(last_name__unaccent__icontains=query)
                result |= result_filter_field.filter(email__icontains=query)

        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_form'] = UserFilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        context['users_active'] = True

        return context
        
@login_required
def users(request):
    users = CustomUser.objects.all()
    users_json = serializers.serialize('json', users)
    context = {
        'Users': users,
        'Users_JSON': users_json,
        'users_active': True,
        }
    #print(users_json)
    return render(request, 'hospital_app/users.html', context)

@login_required
def profile(request, user_id):
    u = get_object_or_404(CustomUser, pk=user_id)
    context = {
        'User': u,
        'profile_active': True,
    }
    return render(request, 'hospital_app/profile.html', context)

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