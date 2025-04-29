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
    is_email_verified = models.BooleanField(default=False)
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
    industry = models.CharField(max_length=255, null=True, blank=True)
    company_size = models.CharField(max_length=100, null=True, blank=True)
    company_address = models.TextField(null=True, blank=True)
    website_url = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.company_name or self.user.name


class ConsultancyProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='consultancy_profile')
    consultancy_name = models.CharField(max_length=255, null=True, blank=True)
    specialization = models.CharField(max_length=255, null=True, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    office_address = models.TextField(null=True, blank=True)
    website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.consultancy_name or self.user.name


class CandidateProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='candidate_profile')
    education = models.CharField(max_length=255, null=True, blank=True)
    experience_years = models.PositiveIntegerField(null=True, blank=True)
    skills = models.TextField(null=True, blank=True)
    resume_url = models.URLField(null=True, blank=True)
    portfolio_website = models.URLField(blank=True, null=True)

    def __str__(self):
        return self.user.name or self.user.name


class EmailOTP(models.Model):
    email = models.EmailField()
    otp = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def is_expired(self):
        return timezone.now() > self.created_at + timedelta(minutes=10)
