from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import User, EmployerProfile, ConsultancyProfile, CandidateProfile

@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        if instance.user_type == 'employer':
            EmployerProfile.objects.create(user=instance)
        elif instance.user_type == 'consultancy':
            ConsultancyProfile.objects.create(user=instance)
        elif instance.user_type == 'candidate':
            CandidateProfile.objects.create(user=instance)
