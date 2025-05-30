# Generated by Django 4.1.5 on 2023-05-01 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exam', '0027_resultpin_use_time_resultpin_used_by'),
    ]

    operations = [
        migrations.CreateModel(
            name='StudentReport',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('event', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='exam.event')),
                ('exam_papers', models.ManyToManyField(to='exam.studentexampaper')),
                ('student', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exam.student')),
            ],
        ),
    ]
