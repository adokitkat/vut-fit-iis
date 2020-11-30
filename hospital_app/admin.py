from django.contrib import admin

from django.contrib.auth import get_user_model
from django.contrib.auth.admin import UserAdmin

from .forms import  CustomUserChangeForm, CustomUserCreationForm
from .models import *
class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ['email', 'first_name', 'last_name', 'role']
    search_fields = ('email', 'first_name', 'last_name')
    exclude = ('username',)
    fieldsets = (
        ('Personal info', {'fields': ('first_name', 'last_name', 'address', 'tel_number', 'email', 'password')}),
        ('Important dates', {'fields': ('last_login', 'date_joined', 'date_birth', 'date_died')}),
        ('Permissions', {'fields': ('role', 'is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'fields': ('email', 'password1', 'password2')}
        ),
    )

    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Problem)
admin.site.register(Ticket)
admin.site.register(HealthRecord)
admin.site.register(File)
admin.site.register(MedicalAct)
admin.site.register(MedicalCompensation)