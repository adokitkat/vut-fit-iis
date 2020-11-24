from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .decorators import admin_required, patient_required, doctor_required, insurance_worker_required, not_patient
from . import views
#from django.views.generic import TemplateView


urlpatterns = [
    path('', views.index, name='index'),
    
    #path('profile/', views.profile, name='profile'),
    path('profile/<int:user_id>/', views.profile, name='profile'),

    path('users/', login_required(not_patient(views.UsersView.as_view(), '', '/')), name='users'), # redirects unauthorizet (Patients) to index

    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]