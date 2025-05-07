from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.db import models
from django.conf import settings
import random
from django.utils import timezone
from datetime import timedelta
class UserManager(BaseUserManager):
    def create_user(self, email, name, phone, user_type, password=None, **extra_fields):
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(email=email, name=name, phone=phone, user_type=user_type, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, name, phone, user_type='admin', password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, name, phone, user_type, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('employer', 'Employer'),
        ('consultancy', 'Consultancy'),
        ('candidate', 'Candidate'),
    )

    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    user_type = models.CharField(max_length=20, choices=USER_TYPES)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_email_verified = models.BooleanField(default=True)
    is_phone_verified = models.BooleanField(default=False)
    is_suspended = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name', 'phone', 'user_type']


    def __str__(self):
        return self.email or self.name



class EmployerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='employer_profile')
    company_name = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    industry = models.CharField(max_length=255, null=True, blank=True)
    company_size = models.CharField(max_length=100, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    website_url = models.URLField(blank=True, null=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)


    # Cloudinary Image Field
    msme_or_incorporation_certificate = models.URLField(null=True, blank=True)
    gstin_certificate = models.URLField(null=True, blank=True)
    pan_card = models.URLField(null=True, blank=True)
    poc_document = models.URLField(null=True, blank=True)

    #application status
    application_status = models.CharField(max_length=255, null=True, blank=True,default='verifying')

    def __str__(self):
        return self.company_name or self.user.name


class ConsultancyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consultancy_profile')
    consultancy_name = models.CharField(max_length=255, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    office_address = models.TextField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)
    consultancy_size = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)

    # Cloudinary Image Field
    msme_or_incorporation_certificate = models.URLField(null=True, blank=True)
    gstin_certificate = models.URLField(null=True, blank=True)
    pan_card = models.URLField(null=True, blank=True)
    poc_document = models.URLField(null=True, blank=True)

    #application status
    application_status = models.CharField(max_length=255, null=True, blank=True,default='verifying')


    def __str__(self):
        return self.consultancy_name or self.user.name


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    skills = models.TextField(null=True, blank=True)
    portfolio_website = models.URLField(blank=True, null=True)
    gender = models.CharField(max_length=10, null=True, blank=True)
    city = models.CharField(max_length=100, null=True, blank=True)
    phone_number = models.CharField(max_length=20, null=True, blank=True)
    preferenced_city = models.CharField(max_length=300, null=True, blank=True)

    # Cloudinary Image Field
    resume = models.URLField(null=True, blank=True)

    #application status
    application_status = models.CharField(max_length=255, null=True, blank=True,default='approved')

    def __str__(self):
        return self.user.name or self.user.name
    
class Education(models.Model):
    EDUCATION_TYPES = (
        ('primary', 'Primary School'),
        ('secondary', 'Secondary School'),
        ('higher_secondary', 'Higher Secondary'),
        ('bachelors', 'Bachelors'),
        ('masters', 'Masters'),
        ('phd', 'PhD'),
        ('other', 'Other'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='educations')
    education_type = models.CharField(max_length=20, choices=EDUCATION_TYPES, default='other')
    school_name = models.CharField(max_length=255, null=True, blank=True)
    degree = models.CharField(max_length=255, null=True, blank=True)
    field_of_study = models.CharField(max_length=255, null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    grade = models.CharField(max_length=50, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.degree} at {self.school_name}"


class Experience(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='experiences')
    company_name = models.CharField(max_length=255, null=True, blank=True)
    designation = models.CharField(max_length=255, null=True, blank=True)
    job_type = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)
    currently_working = models.BooleanField(default=False)
    job_description = models.TextField(null=True, blank=True)
    start_date = models.DateField(null=True, blank=True)
    end_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.created_at:
            self.created_at = timezone.now()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.designation} at {self.company_name}"



class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)
