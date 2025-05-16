from django.db import models
from django.contrib.auth import get_user_model
from accounts.models import User
from accounts.models import EmployerProfile, ConsultancyProfile, CandidateProfile

User = get_user_model()

class JobPost(models.Model):
    JOB_TYPE_CHOICES = [
        ('full-time', 'Full-Time'),
        ('part-time', 'Part-Time'),
        ('freelance', 'Freelance'),
        ('internship', 'Internship'),
        ('contract', 'Contract'),
        ('temporary', 'Temporary'),
    ]

    EXPERIENCE_LEVEL_CHOICES = [
        ('entry', 'Entry Level'),
        ('mid', 'Mid Level'),
        ('senior', 'Senior Level'),
        ('director', 'Director'),
        ('executive', 'Executive'),
        ('lead', 'Lead'),
        ('manager', 'Manager'),
        ('intern', 'Intern'),
    ]

    WORK_MODE_CHOICES = [
        ('remote', 'Remote'),
        ('onsite', 'On-site'),
        ('hybrid', 'Hybrid'),
    ]

    title = models.CharField(max_length=200)
    company_name = models.CharField(max_length=200)
    company_website = models.URLField(blank=True, null=True)
    company_email = models.EmailField(blank=True, null=True)
    company_logo = models.URLField(blank=True, null=True)

    location = models.CharField(max_length=255)
    work_mode = models.CharField(max_length=10, choices=WORK_MODE_CHOICES, default='onsite')

    job_type = models.CharField(max_length=20, choices=JOB_TYPE_CHOICES)
    experience_level = models.CharField(max_length=20, choices=EXPERIENCE_LEVEL_CHOICES)
    industry = models.CharField(max_length=100, blank=True, null=True)

    min_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    max_salary = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    currency = models.CharField(max_length=10, default='INR')  # or USD, EUR, etc.
    salary_type = models.CharField(
        max_length=20,
        choices=[('monthly', 'Monthly'), ('yearly', 'Yearly'), ('hourly', 'Hourly')],
        default='monthly'
    )

    description = models.TextField()
    requirements = models.TextField(blank=True, null=True)
    responsibilities = models.TextField(blank=True, null=True)
    skills_required = models.TextField(help_text="Comma-separated skills", blank=True, null=True)

    deadline = models.DateField(blank=True, null=True)
    vacancies = models.PositiveIntegerField(default=1)

    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='job_posts')
    is_published = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.title} at {self.company_name}"

from django.core.exceptions import ValidationError

class Bid(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ]
    
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='bids')
    consultancy = models.ForeignKey(ConsultancyProfile, on_delete=models.CASCADE, related_name='bids')
    proposal = models.TextField()
    fee = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=['job', 'consultancy', 'proposal'],
                name='unique_bid_proposal'
            )
        ]
    
    def clean(self):
        # Check if consultancy already has 3 bids for this job
        existing_bids = Bid.objects.filter(
            job=self.job, 
            consultancy=self.consultancy
        ).exclude(pk=self.pk)  # Exclude current instance if updating
        
        if existing_bids.count() >= 3:
            raise ValidationError("A consultancy can only submit 3 bids per job")
    
    def save(self, *args, **kwargs):
        self.full_clean()  # Runs clean() validation
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.consultancy.company_name} - {self.job.title}"


class DirectApplication(models.Model):
    STATUS_CHOICES = [
        ('applied', 'Applied'),
        ('shortlisted', 'Shortlisted'),
        ('interview', 'Interview Scheduled'),
        ('rejected', 'Rejected'),
        ('hired', 'Hired'),
        ('pending', 'Pending'),
    ]
    
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='applications')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='applications')
    resume = models.URLField(blank=True, null=True)
    cover_letter = models.TextField(blank=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='applied')
    applied_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        unique_together = ('job', 'candidate')
    
    def __str__(self):
        return f"{self.candidate.get_full_name()} - {self.job.title}"
    

class SavedJob(models.Model):
    job = models.ForeignKey(JobPost, on_delete=models.CASCADE, related_name='saved_jobs')
    candidate = models.ForeignKey(CandidateProfile, on_delete=models.CASCADE, related_name='saved_jobs')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('job', 'candidate')

    def __str__(self):
        return f"{self.candidate.get_full_name()} - {self.job.title}"
