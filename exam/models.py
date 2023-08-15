import string, random
from django.db import models, IntegrityError
from django_summernote.fields import SummernoteTextField
from django.contrib import messages
from address.models import Address
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.conf import settings
from authentication.models import UserAccount
from datetime import timedelta, date, datetime, timezone
from configurations.models import Policy
from django.http import JsonResponse
from customer_relations.models import Officer
now = datetime.now()
###########################################################

EXAM_TIME = 30

##########################################################

class School(models.Model):
    name = models.CharField(max_length=64)
    address = models.CharField(max_length=128)
    #address = models.ForeignKey(Address, on_delete=models.PROTECT, null=True, blank=True)
    school_type = models.CharField(max_length=16)
    
    @property
    def student_count(self):
        return Student.objects.filter(school=self).count()


    def __str__(self):
        if len(self.name) > 20: 
            return f"{self.name[:20]}..."
        return self.name

class Subject(models.Model):
    name = models.CharField(max_length=32)
    category = models.CharField(max_length=16, choices=(('S', 'Senior'), ('J', 'Junior'), ('P', 'Primary')), default='Senior')
    image = models.ImageField(upload_to='subjects', null=True, blank=True)

    def __str__(self):
        return self.name



class Level(models.Model):
    name = models.CharField(max_length=16, help_text="e.g SS1-SS2, JSS3, Junior, Senior, Star. Each exam may have different categorization groups")
    subjects = models.ManyToManyField(Subject)

    def __str__(self):
        return self.name


class Student(models.Model):
    account = models.OneToOneField(UserAccount, on_delete=models.CASCADE)
    school = models.ForeignKey(School, related_name='students', on_delete=models.SET_NULL, null=True, blank=True)
    level = models.ForeignKey(Level, related_name='students', on_delete=models.PROTECT)
    state = models.CharField(max_length=32)
    teacher_number = models.CharField(max_length=16, null=True, blank=True)
    officer = models.ForeignKey(Officer, on_delete=models.CASCADE, blank=True, null=True)

    def add_level(self):
        pass

    @property
    def full_name(self):
        return self.account.get_full_name()
        
    def __str__(self):
        return f"{self.full_name}"
    
    @property
    def status(self):
        number_of_written_exams = StudentExamPaper.objects.filter(student=self).count()
        number_of_checked_results = Registration.objects.filter(student=self, paid=True).count()

        return {
                "written_count": number_of_written_exams,
                "checked_count": number_of_checked_results
        }

    @property
    def written_count(self):
        number_of_written_exams = StudentExamPaper.objects.filter(student=self).count()
        return number_of_written_exams


    @property
    def paid_count(self):
        number_of_checked_results = Payment.objects.filter(registration__student=self, complete=True, free=False).count()
        return number_of_checked_results
    
    @property
    def checked_count(self):
        number_of_checked_results = Registration.objects.filter(student=self, paid=True).count()
        return number_of_checked_results


    @property
    def checked_result(self):
        return Payment.objects.filter(registration__student=self, free=False, complete=True).exists()

    
    @property
    def join_date(self):
        return self.account.created_on
    
    @property
    def started_exams(self):
        return StudentExamPaper.objects.filter(student=self).exists()

    @property
    def parent_number(self):
        return self.account.profile.guardian_phone_number
    
    def save(self, *args, **kwargs):
        #officer_count = Officer.objects.filter(active=True).count()
        #index = self.pk%3
        #self.officer = Officer.objects.filter(active=True)[index]
        
        super().save(*args, **kwargs)

"""
class StudentReport(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    exams = models.ManyToManyKey(Exam)
"""


class Event(models.Model):
    title = models.CharField(max_length=32, help_text="A name that uniquely describes the contest e.g 2023 Yearly Math Contest for Seniors")
    created_at = models.DateField(auto_now_add=True)
    starts_on = models.DateTimeField()
    ends_on = models.DateTimeField()
    policy = models.ForeignKey(Policy, on_delete=models.SET_NULL, null=True, blank=True)
    levels = models.ManyToManyField(Level, related_name='events')
    image = models.ImageField(upload_to='events', null=True, blank=True)

    @property
    def year(self):
        return self.starts_on.year

    def __str__(self):
        return f"{self.title}"

    @property
    def total_payment(self):
        exams = Exam.objects.filter(event=self)
        count = 0
        for i in exams:
            
            count += i.payment_count_
        return f'{count * 500}'
    
    @property
    def policy_(self):
        if self.policy:
            return self.policy
        else:
            return {"exam_duration": 30, "number_of_questions": 40, "registration_limit": 5}


    @property
    def active(self):
        if now < self.ends_on and now > self.starts_on:
            return True
        return False

    ## EVENT SETUP

    def create_all_exams(self):
        for level in Level.objects.all():
            for subject in level.subjects.all():
                Exam.objects.create(event=self, level=level, subject=subject)


    def assign_questions_to_exam(self, exam, count):
        subject = exam.subject
        try:
            questions = random.sample(set(Question.objects.filter(subject=subject)), 100)
    
        ##  CREATE EXAM QUESTIONS
            i = 1
            for q in questions:
                ExamQuestion.objects.create(question=q, exam=exam, order=i)
                print(f" Question {i} - {exam}")

                i += 1

        except ValueError:
            print(f"Value issues - {exam}")

        #except IntegrityError:
        #    print("Already Created")


    def assign_questions_to_all_exams(self, question_count):

        for exam in self.exams.all():
            print(f"Assigning questions to :{exam}")
            self.assign_questions_to_exam(exam, question_count)

    
    def default_setup(self):
        #try:
        #    self.create_all_exams()
        #except IntegrityError:
        #    print("Already created")
        self.assign_questions_to_all_exams(100)
#############                       ##########          #########




class ChoiceSet(models.Model):
    a = models.CharField(max_length=512)
    b = models.CharField(max_length=512)
    c = models.CharField(max_length=512, null=True, blank=True)
    d = models.CharField(max_length=512, null=True, blank=True)
    e = models.CharField(max_length=512, null=True, blank=True)
    f = models.CharField(max_length=512, default='', editable=False)

    class Meta:
        verbose_name_plural = 'Choice Sets'

    def __str__(self):
        str_ = ''
        list_ = []
        for i in (self.a, self.b, self.c, self.d, self.e):
            if i:
                str_ += ' *' + i[:10]
                list_.append(i)

        return f"{list_}"


class Question(models.Model):
    subject = models.ForeignKey(Subject, related_name='questions', on_delete=models.CASCADE)
    question_text = SummernoteTextField()
    choice_set = models.ForeignKey(ChoiceSet, related_name='questions', on_delete=models.CASCADE,null=True, blank=True, verbose_name="options")
    correct_answer = models.CharField(max_length=1, choices=(('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')), null=True, blank=True)

    def __str__(self):
        return f"{self.subject}    -   {self.question_text[:50]}   -   {self.choice_set}"
    @property
    def question_display(self):
        return self.question_text[:30]
    @property
    def category(self):
        return self.subject.category

    class Meta:
        verbose_name_plural = 'Question Bank'


class Exam(models.Model):
    event = models.ForeignKey(Event, related_name='exams', on_delete=models.PROTECT, help_text="Every exam must belong to an event")
    level = models.ForeignKey(Level, related_name='exams', on_delete=models.PROTECT)
    subject = models.ForeignKey(Subject, related_name='exams', on_delete=models.CASCADE)
    students = models.ManyToManyField(Student, related_name='exams', through='Registration')
    #duration = models.DurationField(default=timedelta(minutes=EXAM_TIME))

    def __str__(self):
        
        return f"{self.level} - {self.subject} - {self.event}"

    class Meta:
        unique_together = ('event', 'level', 'subject')
    
    @property
    def student_count(self):
        return self.students.all().count()

    @property
    def payment_count(self):
        return Payment.objects.filter(amount=500, registration__exam=self).count()
    @property
    def payment_count_(self):
        types = ('PIN', 'Paystack',)
        return Payment.objects.filter(amount=500, registration__exam=self, payment_type__name__in=types).count()

    @property
    def duration(self):
        return self.event.policy.exam_duration

    def save(self, *args, **kwargs):
        if not self.subject in self.level.subjects.all():
            print(f"{self.subject} does not belong to the {self.level} level")
        
        super().save(*args, **kwargs)
    
    @property
    def paid_students(self):
        paid_registrations = Registration.objects.filter(exam=self, paid=True)
        
        students = []
        for registration in paid_registrations:
            students.append(registration.student)

        return students


class ExamQuestion(models.Model):
    exam = models.ForeignKey(Exam, related_name='exam_questions', on_delete=models.CASCADE)
    order = models.IntegerField()
    question = models.ForeignKey(Question, related_name='exam_questions', on_delete=models.CASCADE)

    class Meta:
        unique_together = ('exam', 'order')
        verbose_name_plural = 'Exam Questions'

    def __str__(self):
        return f"{self.exam} - Question No. {self.order}"

    @property
    def answer(self):
        return self.question.correct_answer

class StudentExamQuestion(models.Model):
    student = models.ForeignKey(Student, related_name='student_exam_questions', on_delete=models.CASCADE)
    question = models.ForeignKey(ExamQuestion, related_name='student_exam_questions', on_delete=models.CASCADE)
    answer = models.CharField(max_length=2, choices=(('A', 'A'), ('B', 'B'), ('C', 'C'), ('D', 'D'), ('E', 'E')), null=True, blank=True)#, editable=False)
    answer_text = models.TextField(max_length=1024, null=True, blank=True)
    
    def subject_id(self):
        return self.question.exam.subject.pk
        
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)

    #def save(self, *args, **kwargs):
    #    self.subject = self.question.exam.subject
    #    super(StudentExamQuestion, self).save(*args, **kwargs)

    class Meta:
        unique_together = ('student', 'question', 'subject')
        verbose_name_plural = 'Student Exam Questions'

    

    @property
    def question_number(self):
        return self.question.order

    @property
    def correct_answer(self):
        return self.question.question.correct_answer

    @property
    def is_correct(self):
        if self.answer == self.question.question.correct_answer:
            return True
        return False

    @property
    def owner(self):
        return self.student.account

    def __str__(self):

        return f"{self.question} - Answer : {self.answer}"
        
      
class StudentExamPaper(models.Model):
    student = models.ForeignKey(Student, related_name='student_exam_papers', on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, related_name='student_exam_papers', on_delete=models.CASCADE)
    answer_sheet = models.ManyToManyField(StudentExamQuestion)
    score = models.IntegerField(default=0, null=True, blank=True)
    submission_time = models.DateTimeField(auto_now_add=True, null=True, blank=True)

     # PREVENT REGISTERING FOR THE WRONG LEVEL
    def save(self, *args, **kwargs):
        #self.score = self.final_score
        super().save(*args, **kwargs)

    class Meta:
        unique_together = ('student', 'exam')
        verbose_name_plural = 'Student Exam Papers'

    def __str__(self):
        return f"{self.student} - {self.exam}"

    @property
    def final_score(self, *args, **kwargs):
        total = 0
       
        for question in self.answer_sheet.all():
            if question.is_correct:
                total += 1
        #self.score = total
        #super().save(*args, **kwargs)
       
      
        return total
    
    @property
    def percentage(self):
        return f'{self.final_score *100/40}%'

    @property
    def school(self):
        return self.student.school

    @property
    def owner(self):
        return self.student.account
   
    @property
    def is_paid(self):
        return Registration.objects.filter(student=self.student, exam=self.exam, paid=True).exists()

    @property
    def subject_rank(self):
        #final = []
        #papers = StudentExamPaper.objects.filter(exam=self.exam).order_by('-score')
        try:
            papers = StudentExamPaper.objects.filter(exam=self.exam, student__in=self.exam.paid_students).order_by('-score')
        #for i in papers:
        #    if i.is_paid:
        #        final.append(i)
        #final = final.order_by('-score')
            rank = list(papers).index(self) + 1
        except:
            return 0
        return rank

    @property
    def state_rank(self):
        state = self.student.state


        paid_state_students = chain( Student.objects.filter(state=state), self.exam.paid_students)
        try:
            papers = StudentExamPaper.objects.filter(exam=self.exam, student__in=paid_state_students).order_by('-score')
        #for i in papers:
        #    if i.is_paid:
        #        final.append(i)
        #final = final.order_by('-score')
            rank = list(papers).index(self) + 1
        except:
            return 0
        return rank



class Registration(models.Model):
    student = models.ForeignKey(Student, related_name="registrations", on_delete=models.CASCADE)
    exam = models.ForeignKey(Exam, related_name="registrations", on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    paid = models.BooleanField(default=False, editable=False)

    def __str__(self):
        return f"{self.student} {self.exam} Registration"

    #@property
    #def paid(self):
    #    return self.payment.complete
    MAXIMUM_REGISTRATION_COUNT = 5

    @property
    def event(self):
        return self.exam.event

    def save(self, *args, **kwargs):
        def less_than_maximum_registration(student, event):
            exams = event.exams.all()   #EXAMS THAT BELONG TO THAT EVENT
            registration_count = student.registrations.filter(exam__in=exams).count()
            if registration_count <= settings.MAXIMUM_REGISTRATION_COUNT:
                return True
            return False
        #event = Event.objects.get()
        #student = Student.objects.get(id=obj.t)
        if not less_than_maximum_registration(self.student, self.exam.event):
            #messages.set_level(self.request, messages.ERROR)
            #messages.error(self.request, f"You can't register more than {settings.MAXIMUM_REGISTRATION_COUNT} exams")
            return JsonResponse({"msg":f"You can't register more than {settings.MAXIMUM_REGISTRATION_COUNT} exams"})

        #   STUDENT CAN ONLY REGISTER FOR EXAMS IN HIS LEVEL
        if self.student.level == self.exam.level:
            super().save(*args, **kwargs)
            
        else:
            #   REMOVE SUCCESS MESSAGE
            #messages.set_level(self.request, messages.ERROR)
            #print("Please pick an exam in your level")
            #   DISPLAY ERROR MESSAGE
            #print("HANDLE ERROR!!")
            return JsonResponse({"msg":"Please pick an exam in your level"})
    
        
    class Meta:
        unique_together = ('student', 'exam')

class PaymentType(models.Model):
    name = models.CharField(max_length=16)
    
    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Payment Types'


class Payment(models.Model):
    registration = models.OneToOneField(Registration, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    free = models.BooleanField(default=False)
    complete = models.BooleanField(default=False)
    payment_type = models.ForeignKey(PaymentType, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return f"{self.registration} {'Paid' if self.complete else 'Unpaid'}"

    def save(self, *args, **kwargs):
        #   CHECK IF STUDENT HAS MORE THAN MAXIMUM FREE (ONE) PAYMENTS
        exam = self.registration.exam
        event = exam.event
        student = self.registration.student
        registrations = student.registrations.all() # ALL REGISTRATIONS OF THE STUDENT
        current_registrations = registrations.filter(exam__in=event.exams.all())
        current_payments = Payment.objects.filter(registration__in=current_registrations)
        current_payment_count = current_payments.count()

        #   IF FREE, CONVERT AMOUNT TO ZERO
        if self.free:
            self.amount = 0

        #   CURRENT FREE PAYMENTS MEANS PAYMENTS THAT ARE BOTH FREE AND COMPLETED 
        current_free_payments = current_payments.filter(free=True).filter(complete=True)


        def already_saved(self):    #   IF ALREADY GIVEN FREE PAYMENT IS BEING UPDATED
            val = current_free_payments.filter(registration=self.registration).exists()
            #print("VAL :", val)


        #   IF MAXIMUM CONSTRAINT IS MET, THE CURRENT PAYMENT IS FREE AND THE CURRENT PAYMENT IS NOT AMONG THE CURRENT FREE PAYMENTS
        if current_free_payments.count() >= settings.MAXIMUM_FREE_PAYMENTS and self.free and not already_saved(self):
        
            error = "You only have one free payment"
            #print(error)
            return error
            
        elif self.complete == True or self.free == True:
            self.complete = True
            self.registration.paid = True
            self.registration.save()
            super().save(*args, **kwargs)
        else:
            self.registration.paid = False
            self.registration.save()
            super().save(*args, **kwargs)


class ResultPin(models.Model):
    title = models.CharField(max_length=16)
    used = models.BooleanField(default=False)
    pin = models.CharField(max_length=32)
    used_by = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    use_time = models.DateTimeField(null=True, blank=True)
    def generate_pin(self):
        letters = string.ascii_uppercase
        return (self.title + ( ''.join(random.choice(letters) for i in range(16)) ))

    def use(self):
        self.used = True

    def save(self, *args, **kwargs):
        if len(self.pin) >= len(self.title):
            pin = self.pin
        else:
            pin = self.generate_pin()
        self.pin = pin
        super().save(*args, **kwargs)

    def __str__(self):
        return f'{self.title}-{self.pin[-5:]}'

    class Meta:
        verbose_name_plural = 'Result Pins'




class StudentReport(models.Model):
    event = models.ForeignKey(Event, on_delete=models.PROTECT)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    exam_papers = models.ManyToManyField(StudentExamPaper)
    average = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)
    real_average = models.DecimalField(decimal_places=2, max_digits=5, null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Student Reports'

    
    def save(self, *args, **kwargs):
        self.real_average = self.real_average_score
        self.average = self.average_score
        super().save(*args, **kwargs)
    
    @property
    def real_average_score(self):
        count = 0
        total = 0
        for i in self.exam_papers.all():
            count += 1
            total += i.score
        if count > 0:
            return total/count
        return 0

    @property
    def average_score(self):
        count = 0
        total = 0
        for i in self.exam_papers.all():
            if i.is_paid:
                count += 1
                total += i.score
        if count > 0:
            return total/count
        return 0


