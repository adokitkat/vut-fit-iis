from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser
import datetime

class CustomUserCreationForm(UserCreationForm):

  first_name = forms.CharField(required=True, max_length=150, help_text='First name help text', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'First Name widget text'}),)
  last_name = forms.CharField(required=True, max_length=150, help_text='Last name help text', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Last Name widget text'}),)
  #date_birth = forms.CharField(required=True, max_length=150, help_text='Last name help text', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select a date'}),)

  address = forms.CharField(required=True, max_length=300, help_text='Address help text', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your address'}),)
  
  date_birth = forms.DateField(label='Date of birth', input_formats=settings.DATE_INPUT_FORMATS, widget=forms.SelectDateWidget(years=[x for x in range(datetime.datetime.now().year, 1900-1, -1)], attrs={'class':'form-control', 'type':'date', 'format': 'yyyy-mm-dd'}))
  #date_birth = forms.DateField(required=True, input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(attrs={'class':'form-control', 'type':'date', 'format': 'yyyy-mm-dd', 'placeholder':'Select a date'}),)
  #date_birth = forms.DateField(label='Date of birth', input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(format='%d-%m-%Y', attrs={'class':'form-control', 'type': 'date'}), years=[x for x in range(1900, datetime.datetime.now().year+1)])

  class Meta(UserCreationForm):
    model = CustomUser
    fields = ('first_name', 'last_name', 'date_birth', 'address', 'email', 'password1', 'password2',) # 

class CustomUserChangeForm(UserChangeForm):

  class Meta:
    model = CustomUser
    fields = ('email',)
