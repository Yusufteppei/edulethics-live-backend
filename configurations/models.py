from django.db import models

# Create your models here.
class Policy(models.Model):
    policy_title = models.CharField(max_length=64, help_text="Use a name that describes the policy")
    exam_duration = models.DurationField()
    number_of_questions = models.IntegerField()
    registration_limit = models.IntegerField()
    result_collection_fees = models.IntegerField()

    class Meta:
        verbose_name_plural = 'Policy Groups'

    def __str__(self):
        return self.policy_title
