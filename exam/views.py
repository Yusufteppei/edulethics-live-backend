from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, redirect
from rest_framework.viewsets import ModelViewSet
from .serializers import *
from .models import *
from rest_framework.permissions import IsAdminUser, AllowAny, IsAuthenticatedOrReadOnly, IsAuthenticated
from .permissions import IsPaid, IsOwner
from rest_framework.views import APIView
from rest_framework.response import Response
from django.http import JsonResponse, HttpResponse
from rest_framework.permissions import SAFE_METHODS
from rest_framework.decorators import api_view
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
import json
import random
from django.core.cache.backends.base import DEFAULT_TIMEOUT
import datetime

CACHE_TTL = getattr(settings, 'CACHE_TTL', DEFAULT_TIMEOUT)
RESULT_CHECK_FEE = 500
# Create your views here.
class EventViewSet(ModelViewSet):
    serializer_class = EventSerializer
    queryset = Event.objects.all()


class StudentViewSet(ModelViewSet):
    serializer_class = StudentSerializer
    queryset = Student.objects.all()
    permission_classes = [ IsAuthenticated ]


class SubjectViewSet(ModelViewSet):
    serializer_class = SubjectSerializer

    def get_queryset(self):
        #level = self.request.query_params.get('level')
        #print('Level : ', level)
        #level_object = Level.objects.get(name=level)

        #if level:
        #    return level_object.subjects.all()
        return Subject.objects.all()


class SchoolViewSet(ModelViewSet):
    serializer_class = SchoolSerializer
    queryset = School.objects.all()
    permission_classes = [ AllowAny ]


class LevelViewSet(ModelViewSet):
    serializer_class = LevelSerializer
    queryset = Level.objects.all()

#    @method_decorator(cache_page(CACHE_TTL))
#    def dispatch(self, request, *args, **kwargs):
#        return super().dispatch(request, *args, **kwargs)



class ChoicesetViewSet(ModelViewSet):
    serializer_class = ChoiceSetSerializer
    queryset = ChoiceSet.objects.all()
    permission_classes = [ IsAdminUser ]


class QuestionViewSet(ModelViewSet):
    serializer_class = QuestionSerializer
    queryset = Question.objects.all()
    permission_classes = [ IsAdminUser ]


class ExamViewSet(ModelViewSet):
    serializer_class = ExamSerializer

    def get_queryset(self):
        level_name = self.request.query_params.get('level')
        level = Level.objects.get(name=level_name)
        try:
            event = self.request.query_params.get('event')
            event = Event.objects.get(title=event)
        except:
            events = []
            for i in Event.objects.all():
                if i.active:
                    event = i
        return Exam.objects.filter(level=level, event=event)
    
    def get_permissions(self):
        if self.request.method in SAFE_METHODS:
            return (IsAuthenticatedOrReadOnly(),)
        return (IsAdminUser(),)

#    @method_decorator(cache_page(CACHE_TTL))
#    def dispatch(self, request, *args, **kwargs):
#        return super().dispatch(request, *args, **kwargs)

class ExamQuestionViewSet(ModelViewSet):
    serializer_class = ExamQuestionSerializer
    permission_classes = ( IsAuthenticated, )

    def get_queryset(self):
        # NO OF QUESTIONS FRONT END WANTS
        no_of_questions = int(self.request.query_params.get('no_of_questions'))
        #   RANDOMLY GENERATE QUESTIONS
        questions = random.sample(range(1, 100), no_of_questions)
        level_name = self.request.query_params.get('level')
        level = Level.objects.get(name=level_name)
        subject_name = self.request.query_params.get('subject')
        subject = Subject.objects.get(name=subject_name)
        
        #for i in Event.objects.all():
        #    if i.active:
        #        event = i

        try:
            event = self.request.query_params.get('event')
            event = Event.objects.get(title=event)
        except:
            events = []
            for i in Event.objects.all():
                if i.active:
                    event = i


        exam = Exam.objects.filter(level=level, subject=subject, event=event).first()
        return ExamQuestion.objects.filter(exam=exam, order__in=questions)

    @method_decorator(cache_page(60 * 20))
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class StudentExamQuestionViewSet(ModelViewSet):
    serializer_class = StudentExamQuestionSerializer
    permission_classes = (AllowAny, )

    def get_queryset(self):
        request_student = Student.objects.get(account=self.request.user)
        return StudentExamQuestion.objects.filter(student=request_student)
    
    def create(self, request, *args, **kwargs):
        #print("Creating studentExamQuestion")
        order = request.data['question']
        #print("Order ", order)
        request_student = Student.objects.get(account=self.request.user)
        subject = Subject.objects.get(name=request.data['subject'])
        #print("Student ", request_student)
        #for i in Event.objects.all():
        #    if i.active:
        #        event = i
        
        try:
            event = self.request.query_params.get('event')
            event = Event.objects.get(title=event)
        except:
            events = []
            for i in Event.objects.all():
                if i.active:
                    event = i


        exam = Exam.objects.filter(level=request_student.level, subject=subject, event=event).first()
        question = ExamQuestion.objects.get(exam=exam, order=order)
        StudentExamQuestion.objects.create(subject=subject, student=request_student,
        question=question, answer=request.data['answer'])
        return super().create(request, *args, **kwargs)
    
#    def get_permissions(self):
#        if self.action == 'post':
#            return (IsOwner(), )
#        return ( IsAdminUser(), )


class StudentExamPaperViewSet(ModelViewSet):
    serializer_class = StudentExamPaperSerializer
    #queryset = StudentExamPaper.objects.all()

    def get_permissions(self):
        if self.method in SAFE_METHODS:
           return ( IsPaid(), )
        return False

    def get_queryset(self):
        #exam = self.request.query_params.get('exam')
        request_student = Student.objects.get(account=self.request.user)
        return StudentExamPaper.objects.filter(student=request_student)

class RegistrationViewSet(ModelViewSet):
    serializer_class = RegistrationSerializer

    def get_queryset(self):
        user = self.request.user
        student = Student.objects.get(account=user)
        #exam = self.request.body.exam
        return Registration.objects.filter(student=student)

    def get_permissions(self):
        if self.request.method in ['POST', 'DELETE']:
            user = self.request.user
        
            return (IsOwner(), )
        return (IsAuthenticated(),)

@api_view(['DELETE', 'POST'])
def register(request):
     
    if request.method == 'DELETE':
        if not Registration.objects.filter(exam=request.data['exam'], student=request.data['student']).exists():
            return JsonResponse({"message": "Registration does not exist"})
        registration = Registration.objects.get(exam=request.data['exam'], student=request.data['student'])
        obj = f'{registration.exam.subject} {request.user.full_name}'
  
        registration.delete()
        return JsonResponse({'message': f'{obj} Deleted'})
    elif request.method == 'POST':
        reg = Registration.objects.create(exam=request.data['exam'], student=request.data['student'])
        return JsonResponse({'id': reg.id, 'message': 'created'})


@api_view(['GET'])
def isPaid(request):
    student = Student.objects.get(account=request.user)
    exam = Exam.objects.get(id=request.data['exam'])
    is_paid = Payment.objects.filter(registration__exam=exam, student=student, compplete=True).exists()
    
class PaymentViewSet(ModelViewSet):
    serializer_class = PaymentSerializer
    #queryset = Payment.objects.all()

    def get_queryset(self):
        user = self.request.user
        student = Student.objects.get(account=user)
        student_registrations = Registration.objects.filter(student=student)
        payments = Payment.objects.filter(registration__in=student_registrations)
        return payments


#   TAILOR MADE VIEWS FOR SMALLER REQUESTS

@cache_page(60 * 60 *3)
@api_view(['GET'])
def school_count(request):
    count = School.objects.all().count()
    return JsonResponse({"count": count})

@cache_page(60 * 60 * 3)
@api_view(['GET'])
def student_count(request):
    count = Student.objects.all().count()
    return JsonResponse({"count": count})


@api_view(['GET', 'POST'])
def student(request):
    if request.method == 'GET':
        student = Student.objects.get(account=request.user)
        if student.school:
            school = student.school.name
        else:
            school = ''
    elif request.method == 'POST':
        data = json.load(request)
        school = School.objects.get(name=data['school'])
        level = Level.objects.get(name=data['level'])
        student = Student.objects.get_or_create(account=request.user, level=level, school=school)
        student = student[0]
        #print("Student : ", student)
    
    return JsonResponse({
        "id": student.id,
        "first_name": student.account.first_name,
        "last_name": student.account.last_name,
        "level": student.level.name,
        "school": school
        })

@api_view(['GET'])
def student_data(request):
    try:
        first_name = request.query_params.get('first')
        last_name = request.query_params.get('last')

        students = Student.objects.filter(account__first_name=first_name, account__last_name=last_name)
    except:
        return JsonResponse({"message": "Invalid Entry"})
    return JsonResponse([{"first_name": s.account.first_name, "last_name": s.account.last_name, "username": s.account.username, "write_count": s.written_count, "paid_count": s.paid_count, "checked_count": s.checked_count} for s in students], safe=False)

#@cache_page(60 * 3)
@api_view(['GET'])
def taken_exams(request):
    student = Student.objects.get(account=request.user)
    #for i in Event.objects.all():
    #    if i.active:
    #        event = i
    try:
        event = self.request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i
   
    event_exams = Exam.objects.filter(event=event)
    papers = StudentExamPaper.objects.filter(exam__in=event_exams, student=student)
    exams = []
    for i in papers:
        exams.append({'exam': { 'subject': i.exam.subject.name, 'level':i.exam.level.name, 'id':i.exam.id}})
    
    return JsonResponse(exams, safe=False)


@api_view(['GET'])
def unpaid_exams(request):
    student = Student.objects.get(account=request.user)
    #for i in Event.objects.all():
    #    if i.active:
    #        event = i

    try:
        event = request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i

    event_exams = Exam.objects.filter(event=event)
    papers = StudentExamPaper.objects.filter(exam__in=event_exams, student=student)
    exams = []
    for i in papers:
        if i.is_paid == False:
            exams.append({'exam': { 'subject': i.exam.subject.name, 'level':i.exam.level.name, 'id':i.exam.id}})

    return JsonResponse(exams, safe=False)



@api_view(['POST'])
def is_taken(request):
    subject = request.data['subject']
    subject = Subject.objects.get(name=subject)
    #for i in Event.objects.all():
    #    if i.active:
    
    #    event = i
    try:
        event = request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i

    level = Level.objects.get(name=request.data['level'])
    exam = Exam.objects.get(subject=subject, event=event, level=level)
    student = Student.objects.get(account=request.user)
    return JsonResponse({ "taken": StudentExamPaper.objects.filter(exam=exam, student=student).exists()})


@api_view(['GET'])
def paid_exams(request):
    student = Student.objects.get(account=request.user)
    #for i in Event.objects.all():
    #    if i.active:
    #        event = i
    
    try:
        event = request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i

    event_exams = Exam.objects.filter(event=event)
    registrations = Registration.objects.filter(student=student, exam__in=event_exams)
    paid_exams = []
    for r in registrations:
        if r.paid:
            paid_exams.append(r.exam)
    papers = StudentExamPaper.objects.filter(exam__in=paid_exams, student=student)
    exams = []
    for i in papers:
        rank = list(StudentExamPaper.objects.all().order_by('-score')).index(i)+1
        percentage = i.final_score * 100/40
        exams.append({'exam': { 'subject': i.exam.subject.name, 'rank': rank, 'percentage': percentage, 'level':i.exam.level.name, 'id':i.exam.id}})

    return JsonResponse(exams, safe=False)

#@cache_page(60 * 60 * 100)
@api_view(['POST', 'GET'])
def school(request):
    if request.method == 'GET':
        user = request.user
        student = Student.objects.get(account=user)
        school = student.school
        return JsonResponse({
            "id": school.id,
            "name": school.name,
            "school_type": school.school_type
        })
    elif request.method == 'POST':
        request_body = request
        school_data = json.load(request_body)
        if not School.objects.filter(name=school_data['name']).exists():
            #print("Saving new school : ", school_data)
            school = School.objects.create(name=school_data['name'], address=school_data['address'],
            school_type=school_data['school_type'])
            return JsonResponse({
                "id": school.id,
                "name": school.name,
                "address": school.address,
                "school_type": school.school_type
            })
        else:
            
            #print("School already exists")
            return JsonResponse({
                "message": "School already in the database"
            })

@api_view(['POST'])
def check_username_availability(request):
    data = request.body
    if UserAccount.objects.filter(username=data['username']).exists():
        return JsonResponse({
            "message": "username is unavailable"
        })
    else:
        return JsonResponse({
            "message": "username is available"
            })

@api_view(['GET'])
def get_pins(request):
    number_of_pins = request.query_params.get('count')
    title = request.query_params.get('prefix')
    ACCESS_KEY = request.query_params.get('ACCESS_KEY')

    if ACCESS_KEY == 'YUSUF':
        pins = []
        for i in range(int(number_of_pins)):
            p = ResultPin.objects.create(title=title)
            pins.append(p.pin)
        context = {
            'pins': pins
        }
        return JsonResponse(context, safe=False)


@api_view(['POST'])
def pay_with_pin(request):
    pin = request.data['pin']
    user = request.user
    student = Student.objects.get(account=user)
    exam_id = request.data['exam']
    exam = Exam.objects.get(id=exam_id)
    try:
        rp = ResultPin.objects.get(pin=pin)
    except ObjectDoesNotExist:
        return JsonResponse({
            "message": "Pin Unavailable"})
    registration = Registration.objects.get_or_create(student=student, exam=exam)[0]
    #print("REGISTRATION\n\n\n",registration, "\n\n\n")   
    pin_payment = PaymentType.objects.get(name='PIN')

    if rp.used == False:
        rp.used = True
        rp.used_by = student
        rp.use_time = datetime.datetime.now()
        rp.save()
       
        pin_payment = PaymentType.objects.get(name='PIN')

        registration.paid = True
        registration.save()
        #registration = Registration.objects.get(student=student, exam=exam)
        p = Payment.objects.create(registration=registration, amount=500, payment_type=pin_payment, complete=True)
        
        p.save()
       # Payment.objects.create(registration=registration, amount=500, complete=True, payment_type=pin_payment)

        return JsonResponse({
            "message": "Pin Valid. You can check your results now"
        })
    else:
        return JsonResponse({
            "message": "Pin is invalid."
        })
@api_view(['POST'])
def pay_free(request):
    student = request.user.student
    exam_id = request.data['exam']
    exam = Exam.objects.get(id=exam_id)
    registration = Registration.objects.get_or_create(student=student, exam=exam)[0]
    payment = Payment.objects.create(registration=registration, free=True)
    
    return JsonResponse({"message": "Payment Created"})

@api_view(['POST'])
def pay_with_paystack(request):
    student = request.user.student
    exam_id = request.data['exam']
    exam = Exam.objects.get(id=exam_id)
    registration = Registration.objects.get_or_create(student=student, exam=exam)[0]
    paystack_payment = PaymentType.objects.get(name='Paystack')
    payment = Payment.objects.create(registration=registration, amount=RESULT_CHECK_FEE, payment_type=paystack_payment, complete=True)

    return JsonResponse({"message": "Payment Created"})



@api_view(['POST'])
def submit_answers(request):
    student = request.user.student
    data = request.data['answers']
    subject_name = request.data['subject']
    subject_name = subject_name.replace("%20", " ")
    subject = Subject.objects.get(name=subject_name)
    
    try:
        event = request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i

    exam = Exam.objects.get(subject=subject, event=event, level=student.level)
    ##StudentExamPaper.objects.create(exam=exam, student=student)
    for i in data:
        question_id = i['order']
        answer = i['answer']
        question = ExamQuestion.objects.get(exam=exam, order=question_id)
        
    ########    CLEAN UP    ########            
        StudentExamQuestion.objects.create(question=question, answer=answer, subject=subject, student=student)
    for i in StudentExamPaper.objects.all():
        if i.score == 0:
            i.score = i.final_score
            i.save()
    ##############################        
    return JsonResponse({
        "message": "Answers Submitted",
        "answers": data })

@api_view(['GET'])
def has_written_all(request):
    student = Student.objects.get(account=request.user)
    
    try:
        event = request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i

    count = StudentExamPaper.objects.filter(student=student, exam__event=event).all().count()

    if count >=5 :
        return JsonResponse({'completed': 1})
    return JsonResponse({'completed': 0})


@api_view(['GET'])
def has_used_free_payment(request):
    try:
        event = request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i

    student = Student.objects.get(account=request.user)
    used = Payment.objects.filter(registration__exam__event=event, registration__student=student, complete=True, free=True).exists()
    return JsonResponse({'used': used})

@cache_page(60*60*24)
@api_view(['GET'])
def get_top_students_per_exam(request):
    #student = Student.objects.get(account=request.user)
    #level = student.level
    level = request.query_params.get('level')
    level = Level.objects.get(name=level)

    try:
        event = request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i


    exams = level.exams.filter(event=event)
    
    tops = []

    for exam in exams:
        #if StudentExamPaper.objects.filter(exam=exam, student=student).exists():
            #personal_paper = StudentExamPaper.objects.get(exam=exam, student=student)
            #if personal_paper.is_paid:
                #personal_score = {'student': personal_paper.student.full_name, 'school': personal_paper.student.school.name, 'score': personal_paper.final_score, 'rank': personal_paper.subject_rank}

            #else:
                #personal_score = {'student': personal_paper.student.full_name, 'school': personal_paper.student.school.name, 'score': 'Locked', 'rank': 'Locked'}
        top_20 = StudentExamPaper.objects.filter(exam=exam, student__in=exam.paid_students).order_by('-score')[:20]
        top_20_dict = [ {'id': i.id, 'rank':list(top_20).index(i) + 1, 'student': i.student.full_name,'school': i.student.school.name, 'score': i.score} for i in top_20 ]
        #if StudentExamPaper.objects.filter(exam=exam, student=student).exists():
        tops.append({ 'id': exam.id, 'subject': exam.subject.name, 'scores': top_20_dict })
        #else:
            #tops.append({ 'id': exam.id, 'subject': exam.subject.name, 'scores': top_20_dict })
    return JsonResponse(tops, safe=False)


@api_view(['GET'])
def get_top_students_per_exam_state(request):
    #student = Student.objects.get(account=request.user)
    #level = student.level
    level = request.query_params.get('level')
    level = Level.objects.get(name=level)

    try:
        event = request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i


    exams = level.exams.filter(event=event)

    tops = []

    for exam in exams:
        #if StudentExamPaper.objects.filter(exam=exam, student=student).exists():
            #personal_paper = StudentExamPaper.objects.get(exam=exam, student=student)
            #if personal_paper.is_paid:
                #personal_score = {'student': personal_paper.student.full_name, 'school': personal_paper.student.school.name, 'score': personal_paper.final_score, 'rank': personal_paper.subject_rank}

            #else:
                #personal_score = {'student': personal_paper.student.full_name, 'school': personal_paper.student.school.name, 'score': 'Locked', 'rank': 'Locked'}
        top_20 = StudentExamPaper.objects.filter(exam=exam, student__in=exam.paid_students).order_by('-score')[:20]
        top_20_dict = [ {'id': i.id, 'rank':list(top_20).index(i) + 1, 'student': i.student.full_name,'school': i.student.school.name, 'score': i.score} for i in top_20 ]
        #if StudentExamPaper.objects.filter(exam=exam, student=student).exists():
        tops.append({ 'id': exam.id, 'subject': exam.subject.name, 'scores': top_20_dict })
        #else:
            #tops.append({ 'id': exam.id, 'subject': exam.subject.name, 'scores': top_20_dict })
    return JsonResponse(tops, safe=False)




@api_view(['GET'])
def has_made_real_payment(request):
    student = Student.objects.get(account=request.user)

    try:
        event = request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i

    v = Payment.objects.filter(registration__exam__event=event, registration__student=student, free=False, complete=True).exists()

    return JsonResponse({"has_made_real_payment": v})

@api_view(['GET'])
def exam_count(request):
    try:
        event = request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i

    return JsonResponse({"count": StudentExamPaper.objects.filter(exam__event=event).count()})


@api_view(['GET'])
def events(request):
    try:
        level = request.query_params.get('level')
        level = Level.objects.get(name=level)
        events = level.events.all()
    except:
        events = Event.objects.all()

    return JsonResponse([{"title": event.title, "image_url": event.image.url, "start": date(day=event.starts_on.day, month=event.starts_on.month, year=event.starts_on.year).strftime('%d %B %Y'), "end": date(day=event.ends_on.day, month=event.ends_on.month, year=event.ends_on.year).strftime('%d %B %Y')} for event in events], safe=False)


@api_view(['GET'])
def event(request):
    try:
        event = request.query_params.get('event')
        event = Event.objects.get(title=event)
    except:
        events = []
        for i in Event.objects.all():
            if i.active:
                event = i

    access_key = request.query_params.get('ACCESS_KEY')
    if access_key == 'YUSUF':

        return JsonResponse({"title": event.title, "image_url": event.image.url, "is_active": event.active, "payment": event.total_payment})
    return JsonResponse({"title": event.title, "image_url": event.image.url, "is_active": event.active, "start": date(day=event.starts_on.day, month=event.starts_on.month, year=event.starts_on.year).strftime('%d %B %Y'), "end": date(day=event.ends_on.day, month=event.ends_on.month, year=event.ends_on.year).strftime('%d %B %Y')})


@api_view(['GET'])
def check_result(request):
    student = Student.objects.get(account__username=request.query_params.get('username').lower())
    subject = Subject.objects.get(name=request.query_params.get('subject'))
    event = Event.objects.get(title=request.query_params.get('event'))
    
    exam = Exam.objects.get(event=event,level=student.level, subject=subject)
    try:
        exam_paper = StudentExamPaper.objects.get(student=student, exam=exam)
        registration = Registration.objects.get_or_create(student=student, exam=exam)[0]
        direct_payment = PaymentType.objects.get(name='Direct')
        payment = Payment.objects.get_or_create(registration=registration)[0]
        payment.amount=RESULT_CHECK_FEE
        payment.payment_type=direct_payment
        payment.complete=True
        payment.save()

    except StudentExamPaper.DoesNotExist:
        return JsonResponse({"message": "Exam was not written by student"})
    #except IntegrityError:
    #    return JsonResponse({"message": "Payment has previously been made"})

    #registration = Registration.objects.get_or_create(student=student, exam=exam)[0]
    #direct_payment = PaymentType.objects.get(name='Direct')
    #Payment.objects.get_or_create(registration=registration, amount=RESULT_CHECK_FEE, payment_type=direct_payment, complete=True)


    return JsonResponse({ "Username": student.account.username, "Exam": f"{subject.name} - {event.title}", "Score": exam_paper.score })



@api_view(['POST'])
def reset_password(request):
    new_password = request.data['new_password']
    account = request.user

    account.password = make_password(new_password)
    account.save()

