from django.db import models
from django.utils.translation import gettext_lazy as _

# Create your models here.

class User(models.Model):
  first_name = models.CharField(max_length=50)
  last_name  = models.CharField(max_length=50)
  address    = models.CharField(max_length=300)
  email      = models.EmailField(max_length=254, blank=True)
  tel_number = models.CharField(max_length=50, blank=True)
  birth_date = models.DateField()

  class Role(models.TextChoices):
    PATIENT = 'P', _('Patient')
    DOC     = 'D', _('Doctor')
    HICW    = 'H', _('Health Insurance Company Worker')
    ADMIN   = 'A', _('Admin')

  role = models.CharField(max_length=1, choices=Role.choices, default=Role.PATIENT)
  
  created  = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
  closed   = models.DateTimeField(blank=True)

  def get_id(self):
    return id

  def get_role(self):
    return self.Role(self.role)

  def __str__(self):
    return self.first_name + ' ' + self.last_name

class Problem(models.Model):
  name        = models.CharField(max_length=50)
  description = models.TextField(blank=True)
  state       = models.CharField(max_length=50)

  created  = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
  closed   = models.DateTimeField(blank=True)

  id_user = models.ForeignKey(User, on_delete=models.CASCADE)

  def __str__(self):
    return self.name + ', ' + User(self.id_user).__str__() + ', ' + self.created

class Ticket(models.Model):
  class Status(models.TextChoices):
    INWAIT = 'Y', _('Inwaiting') # Yearning to happed, my lord
    MISS   = 'M', _('Missed')
    OK     = 'C', _('Completed')
    ABORT  = 'A', _('Aborted') # Canceled

  status      = models.CharField(max_length=1, choices=Status.choices, default=Status.INWAIT)
  description = models.TextField(blank=True)
  exam_date   = models.DateTimeField(blank=True)

  created  = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
  closed   = models.DateTimeField(blank=True)
  
  id_user    = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Patient')
  id_doctor  = models.ForeignKey(User, on_delete=models.CASCADE, related_name='Doctor')
  id_problem = models.ForeignKey(Problem, on_delete=models.CASCADE)

  def __str__(self):
    return self.Status(self.status) + ', ' + User(self.id_user).__str__() + ', ' + User(self.id_doctor).__str__() + ', ' + self.exam_date

  def get_status(self):
    return self.Status(self.status)
class HealthRecord(models.Model):
  comment = models.TextField(blank=True)

  created  = models.DateTimeField(auto_now_add=True)
  modified = models.DateTimeField(auto_now=True)
  closed   = models.DateTimeField(blank=True)
  
  id_problem = models.ForeignKey(Problem, on_delete=models.CASCADE)
  id_ticket  = models.ForeignKey(Ticket, on_delete=models.CASCADE)

def user_directory_path(instance, filename):
    # file will be uploaded to MEDIA_ROOT/user_<id>/<filename>
    return 'user_{0}/{1}'.format(instance.user.id, filename)

class File(models.Model):
  file        = models.FileField(upload_to=user_directory_path) # Mazanie suboru spolu s polozkou v databazi?
  name        = models.CharField(max_length=50)
  description = models.TextField(blank=True)

  created  = models.DateTimeField(auto_now_add=True)
  #modified = models.DateTimeField(auto_now=True)
  closed   = models.DateTimeField(blank=True)
  
  id_health_record = models.ForeignKey(HealthRecord, on_delete=models.CASCADE)

  def __str__(self):
    return self.name
