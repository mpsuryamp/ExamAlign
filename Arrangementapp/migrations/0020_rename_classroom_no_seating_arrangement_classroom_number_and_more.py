# Generated by Django 5.1.4 on 2025-01-03 11:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Arrangementapp', '0019_alter_complaint_user'),
    ]

    operations = [
        migrations.RenameField(
            model_name='seating_arrangement',
            old_name='classroom_NO',
            new_name='classroom_number',
        ),
        migrations.RenameField(
            model_name='seating_arrangement',
            old_name='Exam_Date',
            new_name='exam_date',
        ),
        migrations.RenameField(
            model_name='seating_arrangement',
            old_name='Exam_Name',
            new_name='exam_name',
        ),
        migrations.RenameField(
            model_name='seating_arrangement',
            old_name='Exam_time',
            new_name='exam_time',
        ),
        migrations.RenameField(
            model_name='seating_arrangement',
            old_name='Reg_NO',
            new_name='register_no',
        ),
        migrations.RenameField(
            model_name='seating_arrangement',
            old_name='Seat_NO',
            new_name='seat_number',
        ),
        migrations.RenameField(
            model_name='seating_arrangement',
            old_name='Subject',
            new_name='subject',
        ),
    ]
