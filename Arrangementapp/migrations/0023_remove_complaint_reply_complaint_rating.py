# Generated by Django 5.1.4 on 2025-01-12 08:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Arrangementapp', '0022_remove_examnotification_exam_date_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='complaint',
            name='Reply',
        ),
        migrations.AddField(
            model_name='complaint',
            name='Rating',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
