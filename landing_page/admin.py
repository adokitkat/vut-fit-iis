from django.contrib import admin
from .models import User, Problem, Ticket, HealthRecord, File
# Register your models here.

admin.site.register(User)
admin.site.register(Problem)
admin.site.register(Ticket)
admin.site.register(HealthRecord)
admin.site.register(File)