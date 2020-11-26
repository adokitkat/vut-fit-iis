from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required

from .decorators import *
from .forms import *
from .models import *

from django.http import HttpResponseRedirect
#@login_required
#@permission_required('permission', raise_exception=True)

def signup(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            return redirect('index')
    else:
        form = CustomUserCreationForm()
    return render(request, 'hospital_app/signup.html', {'signup_form': form})

@login_required
def superuser(request):
    if request.method == 'POST':
        superuser_role_form = SuperuserRoleChangeForm(request.POST, instance=request.user)
        if superuser_role_form.is_valid():
            superuser_role_form.save()
            return redirect('superuser')
    else:
        superuser_role_form = SuperuserRoleChangeForm()

    context = {
        'superuser_role_form': superuser_role_form,
        'superuser_active': True
        }

    return render(request, 'hospital_app/superuser.html', context)

@login_required
def index(request):
    o = get_object_or_404(CustomUser, pk=request.user.id)

    context = {
        'Object': o,
        'profile_active': True,
    }

    return render(request, 'hospital_app/user/profile.html', context)


class UsersView(ListView):
    model = CustomUser
    template_name = 'hospital_app/user/users.html'
    context_object_name = 'Objects'

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

class TicketsView(ListView):
    model = Ticket
    template_name = 'hospital_app/ticket/tickets.html'
    context_object_name = 'Objects'

    def get_queryset(self, model=model):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')

        objects = model.objects.all()

        if self.request.user.is_patient(): # If user is patient he sees only his tickets
            problems = Problem.objects.filter(id_user=self.request.user.id)
            result = objects.filter(id_problem__in=[o.id for o in problems])
        elif self.request.user.is_doctor():
            result = objects.filter(id_doctor=self.request.user.id)
        else:
            result = objects

        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_form'] = UserFilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        context['tickets_active'] = True

        return context

class ProblemsView(ListView):
    model = Problem
    template_name = 'hospital_app/problem/problems.html'
    context_object_name = 'Objects'

    def get_queryset(self, model=model):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')

        objects = model.objects.all()

        if self.request.user.is_patient(): # If user is patient he sees only his problems
            result = objects.filter(id_user=self.request.user.id)
        elif self.request.user.is_doctor():
            tickets = Ticket.objects.filter(id_doctor=self.request.user.id)
            result = objects.filter(id__in=[o.id_problem.id for o in tickets])
        else:
            result = objects

        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_form'] = UserFilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        context['problems_active'] = True

        return context

class HealthRecordsView(ListView):
    model = HealthRecord
    template_name = 'hospital_app/health_record/health_records.html'
    context_object_name = 'Objects'

    def get_queryset(self, model=model):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')

        objects = model.objects.all()

        if self.request.user.is_patient(): # If user is patient he sees only his health records
            problems = Problem.objects.filter(id_user=self.request.user.id)
            result = objects.filter(id_problem__in=[o.id for o in problems])

        elif self.request.user.is_doctor():
            tickets = Ticket.objects.filter(id_doctor=self.request.user.id)
            problems = Problem.objects.filter(id__in=[o.id_problem.id for o in tickets])
            result = objects.filter(id_problem__in=[o.id for o in problems])

        else:
            result = objects

        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_form'] = UserFilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        context['hr_active'] = True

        return context

@login_required
def profile(request, o_id):
    o = get_object_or_404(CustomUser, pk=o_id)

    context = {
        'Object': o,
        'profile_active': True,
    }

    return render(request, 'hospital_app/user/profile.html', context)

@login_required
def ticket(request, o_id):
    o = get_object_or_404(Ticket, pk=o_id)

    context = {
        'Object': o,
        'ticket_active': True, 
    }

    return render(request, 'hospital_app/ticket/ticket.html', context)

@login_required
def health_record(request, o_id):
    o = get_object_or_404(HealthRecord, pk=o_id)

    context = {
        'Object': o,
        'hr_active': True, 
    }

    return render(request, 'hospital_app/health_record/health_record.html', context)

@login_required
def problem(request, o_id):
    o = get_object_or_404(Problem, pk=o_id)

    context = {
        'Object': o,
        'problem_active': True, 
    }

    return render(request, 'hospital_app/problem/problem.html', context)

@login_required
def ticket_add(request):
    if request.method == 'POST':
        ticket_form = TicketCreationForm(request.POST)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect('tickets')
    else:
        ticket_form = TicketCreationForm()

    context = {
        'page_title': 'Add ticket',
        'ticket_form': ticket_form,
        }

    return render(request, 'hospital_app/ticket/ticket_form.html', context)

@login_required
def ticket_change(request, o_id):
    o = get_object_or_404(Ticket, id=o_id)
    if request.method == 'POST':
        ticket_form = TicketChangeForm(request.POST, instance=o)
        if ticket_form.is_valid():
            ticket_form.save()
            return redirect('tickets')
    else:
        ticket_form = TicketChangeForm(instance=o)

    context = {
        'page_title': 'Change ticket',
        'ticket_form': ticket_form,
        }

    return render(request, 'hospital_app/ticket/ticket_form.html', context)

@login_required
def health_record_add(request):
    if request.method == 'POST':
        health_record_form = HealthRecordCreationForm(request.POST)
        if health_record_form.is_valid():
            health_record_form.save()
            return redirect('health_records')
    else:
        health_record = HealthRecordCreationForm()

    context = {
        'page_title': 'Add health record',
        'health_record_form': health_record,
        }

    return render(request, 'hospital_app/health_record/health_record_form.html', context)
    
@login_required
def health_record_change(request, o_id):
    o = get_object_or_404(HealthRecord, id=o_id)
    if request.method == 'POST':
        health_record_form = HealthRecordChangeForm(request.POST, instance=o)
        if health_record_form.is_valid():
            health_record_form.save()
            return redirect('health_records')
    else:
        health_record_form = HealthRecordChangeForm(instance=o)

    context = {
        'page_title': 'Change health record',
        'health_record_form': health_record_form,
        }

    return render(request, 'hospital_app/health_record/health_record_form.html', context)

@login_required
def problem_add(request):
    if request.method == 'POST':
        problem_form = ProblemCreationForm(request.POST)
        if problem_form.is_valid():
            problem_form.save()
            return redirect('problems')
    else:
        problem_form = ProblemCreationForm()

    context = {
        'page_title': 'Add problem',
        'problem_form': problem_form,
        }

    return render(request, 'hospital_app/problem/problem_form.html', context)
    
@login_required
def problem_change(request, o_id):
    o = get_object_or_404(Problem, id=o_id)
    if request.method == 'POST':
        problem_form = ProblemChangeForm(request.POST, instance=o)
        if problem_form.is_valid():
            problem_form.save()
            return redirect('problems')
    else:
        problem_form = ProblemChangeForm(instance=o)

    context = {
        'page_title': 'Change problem',
        'problem_form': problem_form,
        }

    return render(request, 'hospital_app/problem/problem_form.html', context)
