# Generated by Django 4.1.5 on 2023-02-24 22:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('customer_relations', '0002_remove_message_student_remove_officer_students_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='message',
            name='settled',
            field=models.BooleanField(default=False),
        ),
    ]
