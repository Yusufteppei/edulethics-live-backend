from django.db import models
from authentication.models import UserAccount
# Create your models here.

class BankAccount(models.Model):
    user_account = models.ForeignKey(UserAccount, on_delete=models.PROTECT)

    active = models.BooleanField(default=False)

    
    def __str__(self):
        return self.account.full_name


    def activate(self):
        self.active = True
        self.save()


    def deactivate(self):
        self.active = False
        self.save()

