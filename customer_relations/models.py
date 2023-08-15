from django.db import models
from authentication.models import UserAccount

# Create your models here.

class MessageCategory(models.Model):
    title = models.CharField(max_length=32)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name_plural = 'Message Categories'


class Officer(models.Model):
    account = models.OneToOneField(UserAccount,related_name='as_officer', on_delete=models.PROTECT)
    student_accounts = models.ManyToManyField(UserAccount, related_name='officer')
    duties = models.ManyToManyField(MessageCategory)
    active = models.BooleanField(default=False)    

    def __str__(self):
        return self.account.full_name

    def save(self):
        acc = self.account

        #  ADMIN PERMISSION GRANT

        acc.is_staff = True
        acc.save()
        super().save()


class Message(models.Model):
    student_account = models.ForeignKey(UserAccount,related_name='messages', on_delete=models.CASCADE)
    message_category = models.ForeignKey(MessageCategory, on_delete=models.PROTECT)
    message = models.TextField(max_length=255)
    settled = models.BooleanField(default=False)
    #officer = models.ForeignKey(Officer, on_delete=models.CASCADE, null=True, blank=True)

    def __str__(self):
        return f'{self.student_account.full_name}'


    #def officer_(self):
    #    for officer in Officer.objects.all():
    #        if self.student_account in officer.student_accounts.all():
    #            return officer

    @property
    def student(self):
        return self.student_account.full_name


class Response(models.Model):
    message = models.ForeignKey(Message, on_delete=models.CASCADE)
    response = models.TextField(max_length=1024)

    def __str__(self):
        return f'Response to {self.message}'

