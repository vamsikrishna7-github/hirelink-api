from django.contrib import admin
from .models import User, EmployerProfile, ConsultancyProfile, CandidateProfile
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'phone', 'user_type', 'is_staff')
    list_filter = ('user_type', 'is_staff')
    search_fields = ('email', 'name', 'phone')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Profile Info', {'fields': ('name', 'phone', 'user_type')}),
        ('Permissions', {'fields': ('is_staff', 'is_active', 'is_superuser', 'groups', 'user_permissions')}),
    )

admin.site.register(User, UserAdmin)
admin.site.register(EmployerProfile)
admin.site.register(ConsultancyProfile)
admin.site.register(CandidateProfile)
