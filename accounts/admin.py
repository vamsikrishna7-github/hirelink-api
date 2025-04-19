from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import User, EmployerProfile, ConsultancyProfile, CandidateProfile


admin.site.site_header = "HireLink Administration"
admin.site.site_title = "HireLink Admin Portal"
admin.site.index_title = "Welcome to HireLink Admin"

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'phone', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')
    search_fields = ('email', 'name', 'phone')
    ordering = ('email',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone', 'user_type')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'user_type', 'password1', 'password2'),
        }),
    )

admin.site.register(User, UserAdmin)
admin.site.register(EmployerProfile)
admin.site.register(ConsultancyProfile)
admin.site.register(CandidateProfile)
