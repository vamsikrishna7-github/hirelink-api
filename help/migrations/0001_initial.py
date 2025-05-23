# Generated by Django 5.2 on 2025-05-20 11:56

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='HelpSupport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(max_length=255)),
                ('message', models.TextField()),
                ('screenshot1', models.URLField(blank=True, null=True)),
                ('screenshot2', models.URLField(blank=True, null=True)),
                ('screenshot3', models.URLField(blank=True, null=True)),
                ('screenshot4', models.URLField(blank=True, null=True)),
                ('screenshot5', models.URLField(blank=True, null=True)),
                ('status', models.CharField(choices=[('open', 'Open'), ('pending', 'Pending'), ('resolved', 'Resolved'), ('closed', 'Closed')], default='open', max_length=255)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
