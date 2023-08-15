from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import *
from django.contrib.auth import get_user_model
from customer_relations.models import *
User = get_user_model()
import random

#@receiver(post_save, sender=User)
#def create_student(sender, created, instance, **kwargs):
#    if created:
#        Student.objects.create(account=instance)

#   CREATE STUDENT EXAM QUESTION FROM EXAM QUESTION
#@receiver(post_save, sender=ExamQuestion)
#def create_student_exam_question(sender, instance, **kwargs):
    ##  ALL REGISTERED STUDENTS WILL HAVE QUESTIONS BUT ONLY THE PAID STUDENTS WILL RECEIVE FROM API
#    students = instance.exam.students

#   CREATE QUESTION FOR ALL REGISTERED STUDENTS
#    for student in students:
#        StudentExamQuestion.objects.create(question=instance, student=student)



#   CREATE STUDENT EXAM PAPER FROM STUDENT QUESTIONS
@receiver(post_save, sender=StudentExamQuestion)
def create_exam_paper(sender, created, instance, *args, **kwargs):
    student = instance.student
    exam = instance.question.exam
    if not created:
        #print("Student Exam Question should not be updated - Useless error only valid for api")
        pass    
    if StudentExamPaper.objects.filter(exam=exam, student=student).exists():
        StudentExamPaper.objects.get(exam=exam, student=student).answer_sheet.add(instance)
    
    else:
        paper = StudentExamPaper.objects.create(exam=exam, student=student)
        paper.save()
        paper.answer_sheet.add(instance)
        paper.save()
    
        ##  SETTLE STUDENT CREATION MESSAGE
    message_category = MessageCategory.objects.get(title='Student Creation')
    try:
        message = Message.objects.get(message_category=message_category, student_account=student.account)
        message.settled = True
        message.save()
    except:
        pass

#   SETTLE STUDENT CREATION MESSAGE AFTER STUDENT CREATION
#@receiver(post_save, sender=Student)
def settle_student_creation_message(sender, created, instance, *args, **kwargs):
    message_category = MessageCategory.objects.get(title='Student Creation')
    student_account = instance.account
    message = Message.objects.get_or_create(message_category=message_category, student_account=student_account)[0]
    message.settled = True
    message.save()


#   CREATE PAYMENT REQUEST MESSAGE AFTER STUDENT CREATION
@receiver(post_save, sender=StudentExamPaper)
def create_payment_request_message(sender, created, instance, *args, **kwargs):
    message_category = MessageCategory.objects.get(title='Result Check Invitation')
    message_text = f"{instance.student.account.full_name} has written {instance.exam.subject}, invite him to check his results"
    count = Officer.objects.all().count() - 1
    v = random.randint(0, count)
    officer = Officer.objects.all()[v]
    if created:
        if not Payment.objects.filter(registration__student=instance.student, free=False, complete=True).exists():
            Message.objects.create(message=message_text, message_category=message_category, student_account=instance.student.account)


#   SETTLE PAYMENT MESSAGE AFTER PAYMENT
@receiver(post_save, sender=Registration)
def settle_payment_invite_message(sender, created, instance, *args, **kwargs):
    message_category = MessageCategory.objects.get(title='Result Check Invitation')
    student_account = instance.student.account
    try:
        message = Message.objects.get(message_category=message_category, student_account=student_account)
        if instance.paid == True:
            message.settled = True
            message.save()
    except:
        pass
