from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.html import format_html
from .models import User, EmployerProfile, ConsultancyProfile, CandidateProfile, Education, Experience

# Admin site customization
admin.site.site_header = "Zyukthi Administration"
admin.site.site_title = "Zyukthi Admin Portal"
admin.site.index_title = "Welcome to Zyukthi Admin"
admin.site.site_url = "https://zyukthi.vercel.app/"

class EducationInline(admin.TabularInline):
    model = Education
    extra = 0
    fields = ('education_type', 'school_name', 'degree', 'field_of_study', 'start_date', 'end_date', 'grade')

class ExperienceInline(admin.TabularInline):
    model = Experience
    extra = 0
    fields = ('company_name', 'designation', 'job_type', 'location', 'currently_working', 'start_date', 'end_date')

class UserAdmin(BaseUserAdmin):
    list_display = ('email', 'name', 'phone', 'user_type', 'is_staff', 'is_active', 'is_email_verified', 
                   'is_phone_verified', 'is_verified', 'is_suspended', 'is_deleted', 'registration_status')
    list_filter = ('user_type', 'is_staff', 'is_active', 'is_email_verified', 'is_phone_verified', 
                  'is_verified', 'is_suspended', 'is_deleted', 'registration_step')
    search_fields = ('email', 'name', 'phone')
    ordering = ('email',)
    actions = ['approve_users', 'reject_users', 'suspend_users', 'unsuspend_users']
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('name', 'phone', 'user_type')}),
        ('Verification Status', {'fields': ('is_email_verified', 'is_phone_verified', 'is_verified')}),
        ('Account Status', {'fields': ('is_active', 'is_staff', 'is_superuser', 'is_suspended', 'is_deleted')}),
        ('Registration Progress', {'fields': ('registration_step', 'completed_steps')}),
        ('Permissions', {'fields': ('groups', 'user_permissions')}),
    )
    
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'name', 'phone', 'user_type', 'password1', 'password2'),
        }),
    )

    def get_inlines(self, request, obj=None):
        if obj and obj.user_type == 'candidate':
            return [EducationInline, ExperienceInline]
        return []

    def registration_status(self, obj):
        if obj.completed_steps:
            return format_html('<span style="color: green;">✓ Complete</span>')
        return format_html('<span style="color: orange;">⚠ In Progress</span>')
    registration_status.short_description = 'Registration Status'

    def approve_users(self, request, queryset):
        queryset.update(is_verified=True, is_active=True)
    approve_users.short_description = "Approve selected users"

    def reject_users(self, request, queryset):
        queryset.update(is_verified=False, is_active=False)
    reject_users.short_description = "Reject selected users"

    def suspend_users(self, request, queryset):
        queryset.update(is_suspended=True)
    suspend_users.short_description = "Suspend selected users"

    def unsuspend_users(self, request, queryset):
        queryset.update(is_suspended=False)
    unsuspend_users.short_description = "Unsuspend selected users"

class EmployerProfileAdmin(admin.ModelAdmin):
    list_display = ('company_name', 'user', 'designation', 'industry', 'company_size', 'application_status', 'document_status')
    list_filter = ('application_status', 'industry', 'company_size')
    search_fields = ('company_name', 'user__email', 'user__name', 'designation')
    readonly_fields = ('user',)
    
    def document_status(self, obj):
        docs = [
            obj.msme_or_incorporation_certificate,
            obj.gstin_certificate,
            obj.pan_card,
            obj.poc_document
        ]
        uploaded = sum(1 for doc in docs if doc)
        return f"{uploaded}/4 Documents"
    document_status.short_description = 'Documents Uploaded'

class ConsultancyProfileAdmin(admin.ModelAdmin):
    list_display = ('consultancy_name', 'user', 'specialization', 'experience_years', 'consultancy_size', 'application_status', 'document_status')
    list_filter = ('application_status', 'specialization', 'consultancy_size')
    search_fields = ('consultancy_name', 'user__email', 'user__name', 'specialization')
    readonly_fields = ('user',)
    
    def document_status(self, obj):
        docs = [
            obj.msme_or_incorporation_certificate,
            obj.gstin_certificate,
            obj.pan_card,
            obj.poc_document
        ]
        uploaded = sum(1 for doc in docs if doc)
        return f"{uploaded}/4 Documents"
    document_status.short_description = 'Documents Uploaded'

class CandidateProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'gender', 'city', 'preferenced_city', 'application_status', 'resume_status')
    list_filter = ('application_status', 'gender', 'city')
    search_fields = ('user__email', 'user__name', 'city', 'preferenced_city')
    readonly_fields = ('user',)
    
    def resume_status(self, obj):
        if obj.resume:
            return format_html('<span style="color: green;">✓ Uploaded</span>')
        return format_html('<span style="color: red;">✗ Missing</span>')
    resume_status.short_description = 'Resume Status'

class EducationAdmin(admin.ModelAdmin):
    list_display = ('user', 'education_type', 'school_name', 'degree', 'field_of_study', 'start_date', 'end_date')
    list_filter = ('education_type', 'start_date', 'end_date')
    search_fields = ('user__email', 'user__name', 'school_name', 'degree', 'field_of_study')

class ExperienceAdmin(admin.ModelAdmin):
    list_display = ('user', 'company_name', 'designation', 'job_type', 'location', 'currently_working', 'start_date', 'end_date')
    list_filter = ('job_type', 'currently_working', 'start_date', 'end_date')
    search_fields = ('user__email', 'user__name', 'company_name', 'designation', 'location')

# Register models with their admin classes
admin.site.register(User, UserAdmin)
admin.site.register(EmployerProfile, EmployerProfileAdmin)
admin.site.register(ConsultancyProfile, ConsultancyProfileAdmin)
admin.site.register(CandidateProfile, CandidateProfileAdmin)
admin.site.register(Education, EducationAdmin)
admin.site.register(Experience, ExperienceAdmin)
