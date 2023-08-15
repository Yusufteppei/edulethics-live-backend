from django.db.models.signals import post_save
from django.dispatch import receiver
from authentication.models import UserAccount
from .models import *
import random

#@receiver(post_save, sender=UserAccount)
def assign_crm(sender, created, instance, *args, **kwargs):
    count = Officer.objects.all().count() - 1
    v = random.randint(0, count)
   
    message_category = MessageCategory.objects.get(title='Student Creation')
    officer = Officer.objects.filter()[v]
    if created:
        officer.student_accounts.add(instance)
        Message.objects.create(student_account=instance, message=f'{instance.full_name.upper()} has created account. Please Confirm that his student account has been created.', message_category=message_category)
