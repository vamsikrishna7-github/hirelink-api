from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, CandidateProfile, Education, Experience, EmployerProfile, ConsultancyProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'employer':
            EmployerProfile.objects.create(user=instance)
        elif instance.user_type == 'consultancy':
            ConsultancyProfile.objects.create(user=instance)
        elif instance.user_type == 'candidate':
            # Create the candidate profile first
            candidate_profile = CandidateProfile.objects.create(user=instance)
            
            # Create empty education record
            Education.objects.create(
                user=instance,
                school_name="",
                degree="",
                field_of_study=""
            )
            
            # Create empty experience record
            Experience.objects.create(
                user=instance,
                company_name="",
                designation=""
            )