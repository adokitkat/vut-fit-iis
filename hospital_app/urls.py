from django.urls import path, include
from . import views
#from django.views.generic import TemplateView


urlpatterns = [
    path('', views.index, name='index'),
    
    path('profile/<int:user_id>/', views.profile, name='profile'),

    path('users/', views.UsersView.as_view(), name='users'),
    #path('users/', views.users, name='users'),

    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]