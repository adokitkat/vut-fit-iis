from django import forms
from django.conf import settings
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import *
import datetime
from crispy_forms.helper import FormHelper
from django.db.models import Q
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

  first_name = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your first name'}),)
  last_name = forms.CharField(required=True, max_length=150, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your last name'}),)
  address = forms.CharField(required=True, max_length=300, widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Your address'}),)
  email = forms.CharField(required=True, help_text='You will use your email as username.', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'foo@bar.org'}),)
  tel_number = forms.CharField(required=False, max_length=50, label='Phone number', widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': '+421 900 123 456'}),)

  date_died = forms.DateField(required=False, label="Date of death",
                widget=forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Date (YYYY-mm-dd)'},
              ))

  date_birth = forms.DateField(required=False, label="Birth date",
                widget=forms.DateInput(
                attrs={'class': 'form-control', 'placeholder': 'Date (YYYY-mm-dd)'},
              ))

  is_active = forms.BooleanField(required=False, initial=True, label='Alive')
  class Meta(UserCreationForm):
    model = CustomUser
    fields = ('first_name', 'last_name', 'email', 'tel_number', 'date_died', 'date_birth', 'is_active',)


class UserFilterForm(forms.Form):

  FILTER_CHOICES = (
      ('all', 'All'),
      ('P', 'Patients'),
      ('H', 'Insurance Co. Workers'),
      ('D', 'Doctors'),
      ('A', 'Admins'),
    )
  
  TABLE_CHOICES = ( #FIXME: not working
    ('all', 'All'),
    ('I', 'ID'),
    ('N', 'Name'),
    ('E', 'E-mail'),
  )
  search = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search'}),)
  filter_field = forms.ChoiceField(choices=FILTER_CHOICES, label="")
  table_field = forms.ChoiceField(choices=TABLE_CHOICES, label="")

class FilterForm(forms.Form):

  table_field = forms.ChoiceField(label="")
  filter_field = forms.ChoiceField(label="")
  search = forms.CharField(required=False, label="", widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Search'}),)

  def __init__(self, *args, **kwargs):
    page = kwargs.pop('page')

    super().__init__(*args, **kwargs)

    FILTER_CHOICES = ()
    TABLE_CHOICES = ()

    if page == 'Users':
      FILTER_CHOICES = (
        ('all', 'All (filter by role)'),
        ('P', 'Patients'),
        ('H', 'Insurance Co. Workers'),
        ('D', 'Doctors'),
        ('A', 'Admins'),
      )

      TABLE_CHOICES = (
        ('all', 'All (search only by field)'),
        ('name', 'Name'),
        ('email', 'E-mail'),
        ('id', 'ID'),
      )
    
    elif page == 'Tickets':
      FILTER_CHOICES = (
        ('all', 'All (filter by status)'),
        ('W', 'Wanted'),
        ('Y', 'Inwaiting'),
        ('M', 'Missed'),
        ('C', 'Completed'),
        ('A', 'Aborted'),
      )

      TABLE_CHOICES = (
        ('all', 'All (search only by field)'),
        ('name', 'Name'),
        ('description', 'Description'),
        ('prob_name', 'Problem name'),
        ('id', 'ID'),
      )

    elif page == 'Problems':
      FILTER_CHOICES = (
        ('all', 'All (filter by state)'),
        ('M', 'In progress'),
        ('C', 'Completed'),
        ('A', 'Aborted'),
      )

      TABLE_CHOICES = (
        ('all', 'All (search only by field)'),
        ('name', 'Name'),
        ('description', 'Descrioption'),
        ('id', 'ID'),
      )
    
    elif page == 'HealthRecords':
      FILTER_CHOICES = (
        ('all', 'All (search only by field)'),
        ('name', 'Name'),
        ('comment', 'Comment'),
        ('id', 'ID'),
      )

    elif page == 'Files':
      FILTER_CHOICES = (
        ('all', 'All (search only by field)'),
        ('name', 'Name'),
        ('patient', 'Patient'),
        ('hr_id', 'Health record ID'),
        ('hr_comment', 'Health record comment'),
        ('problem', 'Problem name'),
        ('description', 'Descrioption'),
        ('id', 'ID'),
      )
    
    elif page == 'MedAct':
      FILTER_CHOICES = (
        ('all', 'All (filter by covered)'),
        ('True', 'Coverable: True'),
        ('False', 'Coverable: False'),
      )

    elif page == 'MedCom':
      FILTER_CHOICES = (
        ('all', 'All (filter by covered)'),
        ('True', 'Covered: True'),
        ('False', 'Covered: False'),
      )
    

    self.fields['filter_field'].choices = FILTER_CHOICES
    self.fields['table_field'].choices = TABLE_CHOICES

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
  exam_date = forms.SplitDateTimeField(required=False, 
                widget=forms.SplitDateTimeWidget(
                date_attrs={'class': 'form-control', 'placeholder': 'Date (YYYY-mm-dd)'},
                time_attrs={'class': 'form-control', 'placeholder': 'Time (hh:mm:ss)'},
              ))

  class Meta:
    model = Ticket
    fields = ['status', 'description', 'exam_date', 'id_doctor', 'id_problem', 'id_medical_acts']

  def __init__(self, *args, **kwargs):
    user = kwargs.pop('user')

    super().__init__(*args, **kwargs)

    doctors = CustomUser.objects.filter(role="D")
    self.fields['id_doctor'].queryset = doctors

    if user:
      if user.is_patient():
        self.fields['status'].choices = (('W', 'Wanted'),)
        problems = Problem.objects.filter(Q(id_user=user.id))

        self.fields['id_problem'].queryset = problems

      else:
        problems = Problem.objects.all()
        medical_act_compensations = MedicalCompensation.objects.filter(linked=False)

        self.fields['id_problem'].queryset = problems
        self.fields['id_medical_acts'].queryset = medical_act_compensations
    else:
      problems = Problem.objects.all()
      medical_act_compensations = MedicalCompensation.objects.filter(linked=False)

      self.fields['id_problem'].queryset = problems
      self.fields['id_medical_acts'].queryset = medical_act_compensations


class TicketChangeForm(forms.ModelForm):

  #description = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Description...'}),)
  exam_date = forms.SplitDateTimeField(required=False, 
                widget=forms.SplitDateTimeWidget(
                date_attrs={'class': 'form-control', 'placeholder': 'Date (YYYY-mm-dd)'},
                time_attrs={'class': 'form-control', 'placeholder': 'Time (hh:mm:ss)'},
              ))

  date_closed = forms.SplitDateTimeField(required=False, 
                widget=forms.SplitDateTimeWidget(
                date_attrs={'class': 'form-control', 'placeholder': 'Date (YYYY-mm-dd)'},
                time_attrs={'class': 'form-control', 'placeholder': 'Time (hh:mm:ss)'},
              ))

  class Meta:
    model = Ticket
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    problems = Problem.objects.all()#filter(pk=self.fields['id_user'].id)
    doctors = CustomUser.objects.filter(role="D")
    medical_act_compensations = MedicalCompensation.objects.filter(linked=False)

    """ 
    instance = kwargs.get("instance")
    if instance:
      if instance.id_user:
        pass
    """

    instance = kwargs.get("instance", None)
    if instance:
      self.fields['id_medical_acts'].queryset = instance.id_medical_acts.all()
    
    self.fields['id_doctor'].queryset = doctors
    self.fields['id_problem'].queryset = problems
    self.fields['id_medical_acts'].queryset |= medical_act_compensations


class HealthRecordCreationForm(forms.ModelForm):

  class Meta:
    model = HealthRecord
    fields = ['comment', 'id_problem',]

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    problems = Problem.objects.all()
    self.fields['id_problem'].queryset = problems

class HealthRecordChangeForm(forms.ModelForm):

  date_closed = forms.SplitDateTimeField(required=False, 
                widget=forms.SplitDateTimeWidget(
                date_attrs={'class': 'form-control', 'placeholder': 'Date (YYYY-mm-dd)'},
                time_attrs={'class': 'form-control', 'placeholder': 'Time (hh:mm:ss)'},
              ))
  
  class Meta:
    model = HealthRecord
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    problems = Problem.objects.all()#filter(pk=self.fields['id_user'].id)
    #tickets = Tickets.objects.all()

    self.fields['id_problem'].queryset = problems
    #self.fields['id_ticket'].queryset = tickets

class ProblemCreationForm(forms.ModelForm):

  class Meta:
    model = Problem
    fields = ['name', 'description', 'id_user']

  def __init__(self, *args, **kwargs):
    user = kwargs.pop('user')

    super().__init__(*args, **kwargs)

    if user:
      if user.is_patient():
        self.fields['id_user'].queryset = CustomUser.objects.filter(pk=user.id)
      else:
        patients = CustomUser.objects.filter(role="P")
        self.fields['id_user'].queryset = patients
    else:
      patients = CustomUser.objects.filter(role="P")
      self.fields['id_user'].queryset = patients

class ProblemChangeForm(forms.ModelForm):

  date_closed = forms.SplitDateTimeField(required=False, 
                  widget=forms.SplitDateTimeWidget(
                  date_attrs={'class': 'form-control', 'placeholder': 'Date (YYYY-mm-dd)'},
                  time_attrs={'class': 'form-control', 'placeholder': 'Time (hh:mm:ss)'},
                ))

  class Meta:
    model = Problem
    fields = '__all__'

  def __init__(self, *args, **kwargs):
    super().__init__(*args, **kwargs)

    patients = CustomUser.objects.filter(role="P")#filter(pk=self.fields['id_user'].id)
    self.fields['id_user'].queryset = patients


class FileCreationForm(forms.ModelForm):

  class Meta:
    model = File
    fields = '__all__'

class MedicalActCreationForm(forms.ModelForm):

  class Meta:
    model = MedicalAct
    fields = '__all__'

class MedicalCompensationForm(forms.ModelForm):

  class Meta:
    model = MedicalCompensation
    fields = '__all__'