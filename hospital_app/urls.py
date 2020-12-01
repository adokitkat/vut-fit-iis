from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth.decorators import login_required
from .decorators import * # superuser_required, admin_required, patient_required, doctor_required, insurance_worker_required, not_patient
from . import views
#from django.views.generic import TemplateView

urlpatterns = [
    path('', views.profile, name='index'),
    path('signup/', views.signup, name='signup'),
    path('doc/', views.doc, name='doc'),

    path('user/', views.profile, name='index'),
    path('user/all/', login_required(doctor_required(views.UsersView.as_view(), '', '/')), name='users'), # redirects unauthorizet (Patients) to index
    path('user/<int:o_id>/', views.profile, name='profile'),
    path('user/<int:o_id>/edit/', views.user_change, name='user_change'),
    path('user/<int:o_id>/delete/', views.user_delete, name='user_delete'),

    path('ticket/', login_required(not_insurance_worker(views.TicketsView.as_view(), '', '/')), name='tickets'),
    path('ticket/<int:o_id>/', views.ticket, name='ticket'),
    path('ticket/add/', views.ticket_add, name='ticket_add'),
    path('ticket/<int:o_id>/edit/', views.ticket_change, name='ticket_change'),
    #path('ticket/<int:o_id>/delete/', views.ticket_delete, name='ticket_delete'),

    path('problem/', login_required(not_insurance_worker(views.ProblemsView.as_view(), '', '/')), name='problems'),
    path('problem/<int:o_id>/', views.problem, name='problem'),
    path('problem/add/', views.problem_add, name='problem_add'),
    path('problem/<int:o_id>/edit/', views.problem_change, name='problem_change'),
    #path('problem/<int:o_id>/delete/', views.problem_delete, name='problem_delete'),
    
    path('health-record/', login_required(not_insurance_worker(views.HealthRecordsView.as_view(), '', '/')), name='health_records'),
    path('health-record/<int:o_id>/', views.health_record, name='health_record'),
    path('health-record/add/', views.health_record_add, name='health_record_add'),
    path('health-record/<int:o_id>/edit/', views.health_record_change, name='health_record_change'),
    #path('health-record/<int:o_id>/delete/', views.health_record_delete, name='health_record_delete'),

    path('file/', login_required(not_insurance_worker(views.FilesView.as_view(), '', '/')), name='files'),
    path('file/<int:o_id>/', views.file_page, name='file'),
    path('file/add/', views.file_add, name='file_add'),
    path('file/<int:o_id>/delete/', views.file_delete, name='file_delete'),

    path('medical-act/', login_required(insurance_worker_required(views.MedicalActsView.as_view(), '', '/')), name='medical_acts'),
    path('medical-act/<int:o_id>/', views.medical_act, name='medical_act'),
    path('medical-act/add/', views.medical_act_add, name='medical_act_add'),
    path('medical-act/<int:o_id>/edit/', views.medical_act_change, name='medical_act_change'),
    path('medical-act/<int:o_id>/delete/', views.medical_act_delete, name='medical_act_delete'),

    path('medical-compensation/', login_required(not_patient(views.MedicalCompensationView.as_view(), '', '/')), name='medical_compensations'),
    path('medical-compensation/<int:o_id>/', views.medical_compensation, name='medical_compensation'),
    path('medical-compensation/add/', views.medical_compensation_add, name='medical_compensation_add'),
    path('medical-compensation/<int:o_id>/edit/', views.medical_compensation_change, name='medical_compensation_change'),
    path('medical-compensation/<int:o_id>/delete/', views.medical_compensation_delete, name='medical_compensation_delete'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('superuser/', views.superuser, name='superuser'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)