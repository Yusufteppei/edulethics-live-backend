# Generated by Django 4.1.5 on 2023-03-17 18:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0023_alter_studentexampaper_score'),
        ('notification', '0002_broadcast_exam_write_requirement_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='broadcast',
            name='viewed_students',
            field=models.ManyToManyField(to='exam.student'),
        ),
    ]
