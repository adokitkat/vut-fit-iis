from django.db import models
from django.contrib.auth.models import AbstractUser #, Group
from django.utils.translation import gettext_lazy as _ # gettext_lazy => wrap __proxy__ in str() in function... bug?
from django.conf import settings
from .managers import CustomUserManager

class CustomUser(AbstractUser): #models.Model
  """
  Custom user model, email used as username

  Default AbstractUser fields:
    first_name,
    last_name, 
    email,
    date_joined,  #date_created  = models.DateTimeField(auto_now_add=True)
    active,       #alive = models.BooleanField(default=True)
    ...
  """
  username = None # Overriding default username
  email = models.EmailField(_('email address'), unique=True, blank=False) # Setting up email for username usage
  first_name = models.CharField(_('first name'), max_length=150, blank=False) # Overriding blank=True
  last_name = models.CharField(_('last name'), max_length=150, blank=False)   # Overriding blank=True

  address    = models.CharField(max_length=300)
  tel_number = models.CharField(_('telephone number'), max_length=50, blank=True, null=True)

  date_birth = models.DateField(_('date of birth'), blank=False, null=True)
  #date_joined
  date_modified = models.DateTimeField(auto_now=True)
  date_died = models.DateTimeField(_('date of death'), blank=True, null=True)
  #active
  
  class Role(models.TextChoices):
    PATIENT = 'P', _('Patient')
    DOC     = 'D', _('Doctor')
    HICW    = 'H', _('Health Insurance Company Worker')
    ADMIN   = 'A', _('Admin')

  role = models.CharField(max_length=1, choices=Role.choices, default=Role.PATIENT)
  
  USERNAME_FIELD = 'email' # Changing username to be same as email
  REQUIRED_FIELDS = [] # Required for SUPERUSERS only - prompt all blank=False (but username & password) when creating a superuser, crash otherwise

  objects = CustomUserManager()

  def get_role(self):
    return str(self.Role(self.role).label)

  def is_patient(self):
    return self.role == 'P'

  def is_doctor(self):
    return self.role == 'D'

  def is_insurance_worker(self):
    return self.role == 'H'

  def is_admin(self):
    return self.role == 'A'

  def __str__(self):
    if str(self.Role(self.role)) == self.Role.ADMIN:
      return self.email + ', ' + self.get_role().upper()
    else:
      return self.get_full_name() + ', ' + self.get_role()

class Problem(models.Model):
  class State(models.TextChoices):
    INPROG = 'M', _('In progress')
    DONE   = 'C', _('Completed')
    ABORT  = 'A', _('Aborted') 

  name        = models.CharField(max_length=50)
  description = models.TextField(blank=True)
  state       = models.CharField(max_length=1, choices=State.choices, default=State.INPROG)

  date_created  = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)
  date_closed   = models.DateTimeField(blank=True, null=True)

  id_user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)

  def get_state(self):
    return str(self.State(self.state).label)

  def __str__(self):
    return 'PROBLEM: ' + self.name + ', STATE: ' + self.state + ', PATIENT: ' + self.id_user.get_full_name() + ', CREATED: ' + str(self.date_created)[:-13] + ', MODIFIED: ' + str(self.date_modified)[:-13]

class MedicalAct(models.Model):
  description = models.TextField(blank=False, null=False)
  coverable = models.BooleanField(blank=False, null=False, default=False)

  def __str__(self):
    return 'Medical act: ' + self.description
  
class MedicalCompensation(models.Model):
  covered = models.BooleanField(blank=False, null=False, default=False)
  linked = models.BooleanField(blank=False, null=False, default=False)
  
  id_medical_act = models.ForeignKey(MedicalAct, on_delete=models.CASCADE)

  def get_description(self):
    return self.id_medical_act.description + ' (' + str(self.id) + ')'

  def __str__(self):
    return 'Compensation for: ' + self.id_medical_act.description + ' (' + str(self.id) + ')'

class Ticket(models.Model):
  class Status(models.TextChoices):
    WANT   = 'W', _('Wanted')
    INWAIT = 'Y', _('Inwaiting') # Yearning to happed, my lord
    MISS   = 'M', _('Missed')
    OK     = 'C', _('Completed')
    ABORT  = 'A', _('Aborted') # Canceled

  status      = models.CharField(max_length=1, choices=Status.choices, default=Status.INWAIT)
  description = models.TextField(blank=True)
  exam_date   = models.DateTimeField(blank=True, null=True)

  date_created  = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)
  date_closed   = models.DateTimeField(blank=True, null=True)
  
  id_doctor  = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='Doctor')
  id_problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
  id_medical_acts = models.ManyToManyField(MedicalCompensation, blank=True)

  def get_status(self):
    return str(self.Status(self.status).label)

class HealthRecord(models.Model):
  comment = models.TextField(blank=True)

  date_created  = models.DateTimeField(auto_now_add=True)
  date_modified = models.DateTimeField(auto_now=True)
  date_closed   = models.DateTimeField(blank=True, null=True)
  
  id_problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

  def __str__(self):
    return 'PATIENT: ' + self.id_problem.id_user.get_full_name()  + ', PROBLEM: ' + self.id_problem.name + ', CREATED: ' + str(self.date_created)[:-13] + ', MODIFIED: ' + str(self.date_modified)[:-13]

class File(models.Model):
  file        = models.FileField(upload_to='uploads/%Y/%m/%d/')
  name        = models.CharField(max_length=50)
  description = models.TextField(blank=True)

  date_created  = models.DateTimeField(auto_now_add=True)
  
  id_health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE)

  def __str__(self):
    return 'NAME: ' + self.name + ', PATIENT: ' + self.id_health_record.id_problem.id_user.get_full_name() + ', CREATED: ' + str(self.date_created)[:-13] 

  def is_img(self):
    return self.file.name.endswith(('.jpg', 'jpeg', '.png', '.bmp'))