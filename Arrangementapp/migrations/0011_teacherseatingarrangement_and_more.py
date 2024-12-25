# Generated by Django 5.1.4 on 2024-12-18 05:36

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Arrangementapp', '0010_classroom_rows'),
    ]

    operations = [
        migrations.CreateModel(
            name='Teacherseatingarrangement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('exam', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Arrangementapp.examdetails')),
                ('exam_hall', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Arrangementapp.classroom')),
                ('teacher', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='Arrangementapp.login')),
            ],
        ),
        migrations.DeleteModel(
            name='Teacher_Seating_Arrangement',
        ),
    ]
