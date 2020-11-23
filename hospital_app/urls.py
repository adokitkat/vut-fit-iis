from django.urls import path, include
from . import views
#from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index, name='index'),
    path('i2/', views.index2, name='index2'),
    path('signup/', views.signup, name='signup'),
    path('accounts/', include('django.contrib.auth.urls')),
]