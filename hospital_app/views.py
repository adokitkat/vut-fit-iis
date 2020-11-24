from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.contrib.auth.decorators import login_required, permission_required

from .decorators import admin_required, patient_required, doctor_required, insurance_worker_required, not_patient, not_doctor, not_insurance_worker
from .forms import CustomUserCreationForm, UserFilterForm
from .models import CustomUser

#from django.http import HttpResponse
#@login_required
#@permission_required('permission', raise_exception=True)

@login_required
def index(request):
    context = {
        'index_active': True,
        }
    return render(request, 'hospital_app/index.html', context)


class UsersView(ListView):
    model = CustomUser
    template_name = 'hospital_app/users.html'
    context_object_name = 'Users'

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
    return render(request, 'hospital_app/signup.html', {'signup_form': form})