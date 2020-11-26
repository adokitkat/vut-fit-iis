from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import CustomUser, Ticket, HealthRecord, Problem, File
import datetime
from crispy_forms.helper import FormHelper
#from crispy_forms.layout import Layout, Submit, Row, Column

class CustomUserCreationForm(UserCreationForm):
  first_name = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your first name'}),)
  last_name = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your last name'}),)
  address = forms.CharField(required=True, max_length=300, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your address'}),)
  date_birth = forms.DateField(required=True, label='Date of birth', widget=forms.SelectDateWidget(years=[x for x in range(datetime.datetime.now().year, 1900-1, -1)], attrs={'class':'form-control', 'type':'date'}))
  #date_birth = forms.CharField(required=True, max_length=150, help_text='Last name help text', widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'placeholder': 'Select a date'}),)
  #date_birth = forms.DateField(required=True, input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(attrs={'class':'form-control', 'type':'date', 'format': 'yyyy-mm-dd', 'placeholder':'Select a date'}),)
  #date_birth = forms.DateField(required=True, label='Date of birth', input_formats=settings.DATE_INPUT_FORMATS, widget=forms.DateInput(format='%d-%m-%Y', attrs={'class':'form-control', 'type': 'date'}), years=[x for x in range(1900, datetime.datetime.now().year+1)])

  email = forms.CharField(required=True, help_text='You will use your email as username.', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'foo@bar.org'}),)
  tel_number = forms.CharField(required=False, max_length=50, label='Phone number', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+421 900 123 456'}),)

  class Meta(UserCreationForm):
    model = CustomUser
    fields = ('first_name', 'last_name', 'date_birth', 'address', 'email', 'tel_number', 'password1', 'password2',) # 

class CustomUserChangeForm(UserChangeForm):

  class Meta:
    model = CustomUser
    fields = ('email',)

class UserFilterForm(forms.Form):

  FILTER_CHOICES = (
      ('all', 'All'),
      ('P', 'Patients'),
      ('H', 'Insurance Co. Workers'),
      ('D', 'Doctors'),
      ('A', 'Admins'),
    )
  search = forms.CharField(required=False, label="")
  filter_field = forms.ChoiceField(choices=FILTER_CHOICES, label="")


class SuperuserRoleChangeForm(UserChangeForm):

  def __init__(self, *args, **kwargs):
    super(SuperuserRoleChangeForm, self).__init__(*args, **kwargs)
    self.helper = FormHelper()
    self.helper.form_show_labels = False 

  class Meta:
    model = CustomUser
    fields = ('role',)

class TicketCreationForm(forms.ModelForm):

  #description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description...'}),)
  exam_date   = forms.SplitDateTimeField(required=False, 
                  widget=forms.SplitDateTimeWidget(
                  date_attrs={'class': 'form-control', 'placeholder': 'Date (YYYY-mm-dd)'},
                  time_attrs={'class': 'form-control', 'placeholder': 'Time (hh:mm:ss)'},
                ))

  class Meta:
    model = Ticket
    fields = ['status', 'description', 'exam_date', 'id_user', 'id_doctor']

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    patients = CustomUser.objects.filter(role="P")
    doctors = CustomUser.objects.filter(role="D")

    """
    instance = kwargs.get("instance")
    if instance:
      if instance.id_user:
        pass
    """
    self.fields['id_user'].queryset = patients
    self.fields['id_doctor'].queryset = doctors


class TicketChangeForm(forms.ModelForm):

  #description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description...'}),)
  exam_date   = forms.SplitDateTimeField(required=False, 
                  widget=forms.SplitDateTimeWidget(
                  date_attrs={'class': 'form-control', 'placeholder': 'Date (YYYY-mm-dd)'},
                  time_attrs={'class': 'form-control', 'placeholder': 'Time (hh:mm:ss)'},
                ))

  class Meta:
    model = Ticket
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    problems = CustomUser.objects.all()#filter(pk=self.fields['id_user'].id)
    doctors = CustomUser.objects.filter(role="D")

    """ 
    instance = kwargs.get("instance")
    if instance:
      if instance.id_user:
        pass
    """

    self.fields['id_doctor'].queryset = doctors
    self.fields['id_problem'].queryset = problems