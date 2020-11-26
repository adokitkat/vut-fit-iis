from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .decorators import superuser_required, admin_required, patient_required, doctor_required, insurance_worker_required, not_patient
from . import views
#from django.views.generic import TemplateView

urlpatterns = [
    path('signup/', views.signup, name='signup'),
    path('', views.index, name='index'),

    path('user/all/', login_required(not_patient(views.UsersView.as_view(), '', '/')), name='users'), # redirects unauthorizet (Patients) to index
    path('user/<int:o_id>/', views.profile, name='profile'),

    path('ticket/all/', login_required(views.TicketsView.as_view(), '', '/'), name='tickets'),
    path('ticket/<int:o_id>/', views.ticket, name='ticket'),
    path('ticket/add/', views.ticket_add, name='ticket_add'),
    path('ticket/<int:o_id>/edit/', views.ticket_change, name='ticket_change'),

    path('problem/all/', login_required(views.ProblemsView.as_view(), '', '/'), name='problems'),
    path('problem/<int:o_id>/', views.problem, name='problem'),
    
    path('health-record/all/', login_required(views.HealthRecordsView.as_view(), '', '/'), name='health_records'),
    path('health-record/<int:o_id>/', views.health_record, name='health_record'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('superuser/', views.superuser, name='superuser'),
]