from django.db import models
from exam.models import Student
from authentication.models import *
#from django.contrib.auth.models import get_user_model
from .models import *
#UserAccount = get_user_model()

# Create your models here.


class Chat(models.Model):
    person1 = models.ForeignKey(Student, related_name='chat_initiators', on_delete=models.CASCADE)
    person2 = models.ForeignKey(Student, related_name='chat_accepters', on_delete=models.CASCADE)
     
    def __str__(self):
        return f'{self.person1}-{self.person2}'

class Message(models.Model):
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    sender = models.ForeignKey(Student, on_delete=models.CASCADE)
    message = models.TextField(max_length=512)
    time_sent = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=True)

    def __str__(self):
        return f'{self.message[:30]} from {self.sender}'



