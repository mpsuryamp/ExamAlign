# Generated by Django 5.1.4 on 2024-12-15 07:02

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('Arrangementapp', '0004_rename_branch_name_branch_branchname_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='subject',
            old_name='Branch',
            new_name='branch',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='Semester',
            new_name='semester',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='Subject_Code',
            new_name='subject_Code',
        ),
        migrations.RenameField(
            model_name='subject',
            old_name='Subject_Name',
            new_name='subject_Name',
        ),
    ]