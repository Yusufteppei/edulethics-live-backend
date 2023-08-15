from django.db import models
from exam.models import Level, Student

# Create your models here.

class Broadcast(models.Model):
    CATEGORIES = (
            ('Info', 'Info'),
            ('Warning', 'Warning'),
            ('Good', 'Good'))

    topic = models.CharField(max_length=64)
    message = models.TextField(max_length=1024)
    levels = models.ManyToManyField(Level, help_text='The classes broadcast concerns')
    category = models.CharField(max_length=32, choices=CATEGORIES)
    
    result_check_requirement = models.IntegerField()
    exam_write_requirement = models.IntegerField()
    time = models.DateTimeField(auto_now_add=True)

    """viewed_students = models.ManyToManyField(Student)


    @property
    def viewed_count(self):
        return self.viewed_students.all().count()
    """

    def __str__(self):
        return f'{self.topic}'
