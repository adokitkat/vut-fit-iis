from django.contrib.auth import authenticate, login
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.contrib.auth.decorators import login_required, permission_required
from django.db.models import Q

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
@superuser_required
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
        
        if query:
            result_filter_field = result_filter_field.filter (
                Q(tel_number__icontains=query) | 
                Q(email__icontains=query) |
                Q(first_name__icontains=query) |
                Q(last_name__icontains=query) |
                Q(pk__icontains=query)
            )
        
        return result_filter_field

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_form'] = UserFilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
            'table_field': self.request.GET.get('table_field', ''),
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
            result_all = objects.filter(id_problem__in=[o.id for o in problems])
        elif self.request.user.is_doctor():
            result_all = objects.filter(id_doctor=self.request.user.id)
        else:
            result_all = objects

        result_filter_field = result_all

        if query:
            result_filter_field = result_filter_field.filter (
                Q(description__icontains=query) | 
                Q(id_problem__name__icontains=query) |
                Q(id_problem__id_user__first_name__icontains=query) |
                Q(id_problem__id_user__last_name__icontains=query) |
                Q(id_doctor__first_name__icontains=query) |
                Q(id_doctor__last_name__icontains=query) |
                Q(pk__icontains=query)
            )

        return result_filter_field

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
            result_all = objects.filter(id_user=self.request.user.id)
        elif self.request.user.is_doctor():
            tickets = Ticket.objects.filter(id_doctor=self.request.user.id)
            tickets_filtered = [o for o in tickets if o.id_problem is not None]
            result_all = objects.filter(id__in=[o.id_problem.id for o in tickets_filtered])
        else:
            result_all = objects

        result_filter_field = result_all

        if query:
            result_filter_field = result_filter_field.filter (
                Q(description__icontains=query) | 
                Q(name__icontains=query) |
                Q(id_user__first_name__icontains=query) |
                Q(id_user__last_name__icontains=query) |
                Q(pk__icontains=query)
            )
        
        return result_filter_field

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
            tickets_filtered = [o for o in tickets if o.id_problem is not None]
            result = objects.filter(id_problem__in=[o.id_problem.id for o in tickets_filtered])
        else:
            result = objects

        if query:
            result = result.filter (
                Q(comment__icontains=query) | 
                Q(id_problem__name__icontains=query) |
                Q(id_problem__id_user__first_name__icontains=query) |
                Q(id_problem__id_user__last_name__icontains=query) |
                Q(pk__icontains=query)
            )

        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_form'] = UserFilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        context['hr_active'] = True

        return context

class FilesView(ListView):
    model = File
    template_name = 'hospital_app/file/files.html'
    context_object_name = 'Objects'

    def get_queryset(self, model=model):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')

        objects = model.objects.all()

        # TODO: if patient or worker redirect
        
        if self.request.user.is_doctor():
            tickets = Ticket.objects.filter(id_doctor=self.request.user.id)
            tickets_filtered_problem_ids = [o.id_problem for o in tickets]

            health_records = HealthRecord.objects.filter(id_problem__in=tickets_filtered_problem_ids)

            #tickets_filtered = [o for o in tickets if o.id_problem is not None]
            #result = objects.filter(id_file__in=[o.id_problem.id for o in tickets_filtered]) 

            result_all = objects.filter(id_health_record__in=[o.id for o in health_records])
        
        elif self.request.user.is_admin():
            result_all = objects
        
        else:
            result_all = objects

        result_filter_field = result_all

        # search

        result = result_filter_field
            
        if query:
            result = result.filter (
                Q(name__icontains=query) | 
                Q(description__icontains=query) |
                Q(id_health_record__comment__icontains=query) |  
                Q(id_health_record__id_problem__name__icontains=query) |
                Q(id_health_record__id_problem__id_user__first_name__icontains=query) |
                Q(id_health_record__id_problem__id_user__last_name__icontains=query) |
                Q(id_health_record__pk__icontains=query) |
                Q(pk__icontains=query)
        )

        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_form'] = UserFilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        context['files_active'] = True

        return context

class MedicalActsView(ListView):
    model = MedicalAct
    template_name = 'hospital_app/medical_act/medical_acts.html'
    context_object_name = 'Objects'

    def get_queryset(self, model=model):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')

        objects = model.objects.all()
        """
        if self.request.user.is_patient(): # If user is patient he sees only his health records
            problems = Problem.objects.filter(id_user=self.request.user.id)
            result = objects.filter(id_problem__in=[o.id for o in problems])

        elif self.request.user.is_doctor():
            tickets = Ticket.objects.filter(id_doctor=self.request.user.id)
            tickets_filtered = [o for o in tickets if o.id_problem is not None]
            result = objects.filter(id_problem__in=[o.id_problem.id for o in tickets_filtered])
        else:
        """
        result = objects

        if query:
            result = result.filter (
                Q(description__icontains=query) |
                Q(pk__icontains=query)
        )

        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_form'] = UserFilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        context['ma_active'] = True

        return context

class MedicalCompensationView(ListView):
    model = MedicalCompensation
    template_name = 'hospital_app/medical_compensation/medical_compensations.html'
    context_object_name = 'Objects'

    def get_queryset(self, model=model):
        query = self.request.GET.get('search')
        filter_field = self.request.GET.get('filter_field')

        objects = model.objects.all()
        """
        if self.request.user.is_patient(): # If user is patient he sees only his health records
            problems = Problem.objects.filter(id_user=self.request.user.id)
            result = objects.filter(id_problem__in=[o.id for o in problems])

        elif self.request.user.is_doctor():
            tickets = Ticket.objects.filter(id_doctor=self.request.user.id)
            tickets_filtered = [o for o in tickets if o.id_problem is not None]
            result = objects.filter(id_problem__in=[o.id_problem.id for o in tickets_filtered])
        else:
        """
        result = objects

        if query:
            result = result.filter (
                Q(id_medical_act__description__icontains=query) |
                Q(pk__icontains=query)
        )

        return result

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context['search_form'] = UserFilterForm(initial={
            'search': self.request.GET.get('search', ''),
            'filter_field': self.request.GET.get('filter_field', ''),
        })
        context['mc_active'] = True

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
def ticket_add(request):
    if request.method == 'POST':
        ticket_form = TicketCreationForm(request.POST)
        if ticket_form.is_valid():
            ticket_form.save()

            ticket = Ticket.objects.last()
            ticket.id_medical_acts.all().update(linked=True) # medical compensations

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

    selected_compensation = o.id_medical_acts.all()
    old_ids = [o.id for o in selected_compensation]

    if request.method == 'POST':
        ticket_form = TicketChangeForm(request.POST, instance=o)
        if ticket_form.is_valid():
            ticket_form.save()

            ticket = Ticket.objects.get(pk=o_id)
            ticket.id_medical_acts.all().update(linked=True) # medical compensations

            new_ids = [o.id for o in ticket.id_medical_acts.all()]
          
            #unlink_ids = [i for i in new_ids + old_ids if i not in new_ids or i not in old_ids]
            #print(unlink_ids)
            unlink_ids = [x for x in old_ids if x not in new_ids]

            if unlink_ids:
                MedicalCompensation.objects.filter(pk__in=unlink_ids).update(linked=False)

            return redirect('tickets')
    else:
        ticket_form = TicketChangeForm(instance=o)

    context = {
        'page_title': 'Change ticket',
        'ticket_form': ticket_form,
        }

    return render(request, 'hospital_app/ticket/ticket_form.html', context)

@login_required
def health_record(request, o_id):
    o = get_object_or_404(HealthRecord, pk=o_id)
    o2 = File.objects.filter(id_health_record=o.id)

    context = {
        'Object': o,
        'hr_active': True, 
        'Files': o2,
    }

    return render(request, 'hospital_app/health_record/health_record.html', context)


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
def problem(request, o_id):
    o = get_object_or_404(Problem, pk=o_id)

    context = {
        'Object': o,
        'problem_active': True, 
    }

    return render(request, 'hospital_app/problem/problem.html', context)


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

@login_required
def file_page(request, o_id):
    o = get_object_or_404(File, pk=o_id)

    context = {
        'Object': o,
        'file_active': True, 
    }

    return render(request, 'hospital_app/file/file.html', context)

@login_required
def file_add(request):
    if request.method == 'POST':
        file_form = FileCreationForm(request.POST, request.FILES)
        if file_form.is_valid():
            file_form.save()
            return redirect('files')
    else:
        file_form = FileCreationForm()

    context = {
        'page_title': 'Add file',
        'file_form': file_form,
        }

    return render(request, 'hospital_app/file/file_form.html', context)

@login_required
def file_delete(request, o_id):
    o = get_object_or_404(File, pk=o_id)
    o.delete()
    return redirect('files')

@login_required
def medical_act(request, o_id):
    o = get_object_or_404(MedicalAct, pk=o_id)

    context = {
        'Object': o,
        'md_active': True, 
    }

    return render(request, 'hospital_app/medical_act/medical_act.html', context)

@login_required
def medical_act_add(request):
    if request.method == 'POST':
        medical_act_form = MedicalActCreationForm(request.POST)
        if medical_act_form.is_valid():
            medical_act_form.save()
            return redirect('medical_acts')
    else:
        medical_act_form = MedicalActCreationForm()

    context = {
        'page_title': 'Add medical act',
        'ma_form': medical_act_form,
        }

    return render(request, 'hospital_app/medical_act/medical_act_form.html', context)

@login_required
def medical_act_change(request, o_id):
    o = get_object_or_404(MedicalAct, id=o_id)
    if request.method == 'POST':
        medical_act_form = MedicalActCreationForm(request.POST, instance=o)
        if medical_act_form.is_valid():
            medical_act_form.save()
            return redirect('medical_acts')
    else:
        medical_act_form = MedicalActCreationForm(instance=o)

    context = {
        'page_title': 'Change medical act',
        'ma_form': medical_act_form,
        }

    return render(request, 'hospital_app/medical_act/medical_act_form.html', context)

@login_required
def medical_act_delete(request, o_id):
    o = get_object_or_404(MedicalAct, pk=o_id)
    o.delete()
    return redirect('medical_acts')

@login_required
def medical_compensation(request, o_id):
    o = get_object_or_404(MedicalCompensation, pk=o_id)

    context = {
        'Object': o,
        'mc_active': True, 
    }

    return render(request, 'hospital_app/medical_compensation/medical_compensation.html', context)

@login_required
def medical_compensation_add(request):
    if request.method == 'POST':
        form = MedicalCompensationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('medical_compensations')
    else:
        form = MedicalCompensationForm()

    context = {
        'page_title': 'Add medical compensation',
        'mc_form': form,
        }

    return render(request, 'hospital_app/medical_compensation/medical_compensation_form.html', context)

@login_required
def medical_compensation_change(request, o_id):
    o = get_object_or_404(MedicalCompensation, pk=o_id)
    if request.method == 'POST':
        form = MedicalCompensationForm(request.POST, instance=o)
        if form.is_valid():
            form.save()
            return redirect('medical_compensations')
    else:
        form = MedicalCompensationForm(instance=o)

    context = {
        'page_title': 'Add medical compensation',
        'mc_form': form,
        }

    return render(request, 'hospital_app/medical_compensation/medical_compensation_form.html', context)

@login_required
def medical_compensation_delete(request, o_id):
    o = get_object_or_404(MedicalCompensation, pk=o_id)
    o.delete()
    return redirect('medical_compensations')
