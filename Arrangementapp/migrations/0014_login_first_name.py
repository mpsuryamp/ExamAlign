# Generated by Django 5.1.4 on 2024-12-18 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Arrangementapp', '0013_staff_profile_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='login',
            name='first_name',
            field=models.CharField(blank=True, max_length=100, null=True),
        ),
    ]
