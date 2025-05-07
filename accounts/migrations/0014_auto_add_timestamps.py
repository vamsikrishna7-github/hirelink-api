from django.db import migrations, models
import django.utils.timezone

def set_default_timestamps(apps, schema_editor):
    Education = apps.get_model('accounts', 'Education')
    Experience = apps.get_model('accounts', 'Experience')
    
    for model in [Education, Experience]:
        for instance in model.objects.all():
            instance.created_at = django.utils.timezone.now()
            instance.updated_at = django.utils.timezone.now()
            instance.save()

class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0013_remove_candidateexperience_candidate_profile_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='education',
            name='created_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='education',
            name='updated_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='experience',
            name='created_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.AddField(
            model_name='experience',
            name='updated_at',
            field=models.DateTimeField(null=True, blank=True),
        ),
        migrations.RunPython(set_default_timestamps),
        migrations.AlterField(
            model_name='education',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='education',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='experience',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ] 