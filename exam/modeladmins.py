from django.contrib import admin
from import_export.admin import ImportExportModelAdmin
from .models import *
from django.contrib import messages
from django_summernote.admin import SummernoteModelAdmin
from django.conf import settings
from django.template.defaultfilters import escape
from django.urls import reverse 
from django.utils.safestring import mark_safe  
@admin.register(Question)
class QuestionAdmin(SummernoteModelAdmin):
    summernote_fields = ('question_text',)
    list_display = ('question_text', 'subject', 'correct_answer')
    list_filter = ('subject', 'correct_answer',)

#   QUESTION
"""
@admin.register(Question)
class QuestionAdmin(SummernoteModelAdmin):

    fieldsets = (
        (
            'Question', { 
                'fields': ('subject', 'question_text'),
                "description": 'This question will not be in an exam until an exam question is created referencing it'
                }
            ),
        ('Answer', { 'fields':('choice_set', 'correct_answer')})
    )

"""
####################
admin.site.register(PaymentType)

@admin.register(ResultPin)
class ResultPinModelAdmin(admin.ModelAdmin):
    list_display = ('pin', 'used', 'used_by', 'use_time')
    list_filter = ('used',)
    search_fields = ('pin', 'used_by__account__first_name', 'used_by__account__last_name')
    search_help_text = "Search by pin or student name"
####################

admin.site.register(UserAccount)

#   EXAM
@admin.register(Exam)
class ExamAdmin(admin.ModelAdmin):
    list_display = ('subject', 'level', 'student_count')
    list_filter = ('event', 'level', 'subject')

    def save_model(self, request, obj, form, change):
        if not obj.subject in obj.level.subjects.all():
            messages.set_level(request, messages.WARNING)
            messages.warning(request, f"{obj.subject} does not belong to the {obj.level} level")
            messages.warning(request, f"Add {obj.subject} to subjects in {obj.level} or change subject")
            return
        obj.save()


#   EXAM QUESTION
@admin.register(ExamQuestion)
class ExamQuestionAdmin(ImportExportModelAdmin):
    list_display = ('exam', 'order', 'answer')
    list_filter = ('exam__event',)
    search_fields = ('exam__event__title', 'exam__subject__name')

    def question_link(self, obj):
        return mark_safe('<a href="{}">{}</a>'.format(
            reverse("admin:exam_question_change", args=(obj.question.pk,)),
            obj.question.question_text
        ))

    question_link.allow_tags = True
    question_link.short_description = "Question"


#   REGISTRATION
@admin.register(Registration)
class RegistrationAdmin(admin.ModelAdmin):
    list_display = ('student', 'exam', 'date', 'paid')
    list_filter = ('exam', 'paid')
    search_fields = ('student__account__first_name', 'student__account__last_name', 'exam__subject__name')
    search_help_text = "Search by student's name or subject"
    #MAXIMUM_REGISTRATION_COUNT = 2

    def save_model(self, request, obj, form, change):
        def less_than_maximum_registration(student, event):
            exams = event.exams.all()   #EXAMS THAT BELONG TO THAT EVENT
            registration_count = student.registrations.filter(exam__in=exams).count()
            if registration_count <= settings.MAXIMUM_REGISTRATION_COUNT:
                return True
            return False
        #event = Event.objects.get()
        #student = Student.objects.get(id=obj.t)
        if not less_than_maximum_registration(obj.student, obj.exam.event):
            messages.set_level(request, messages.ERROR)
            messages.error(request, f"You can't register more than {settings.MAXIMUM_REGISTRATION_COUNT} exams")

        #   STUDENT CAN ONLY REGISTER FOR EXAMS IN HIS LEVEL
        if obj.student.level == obj.exam.level:
            obj.save()
        else:
            #   REMOVE SUCCESS MESSAGE
            messages.set_level(request, messages.ERROR)
            #print("Please pick an exam in your level")
            #   DISPLAY ERROR MESSAGE
            messages.error(request, "Please pick an exam in your level")

#   PAYMENT
@admin.register(Payment)
class PaymentAdmin(ImportExportModelAdmin):
    list_display = ('registration', 'amount', 'complete')
    list_filter = ('complete','free', 'payment_type')
    search_fields = ('registration__student__account__first_name', 'registration__student__account__last_name', 'registration__student__account__username', 'registration__exam__subject__name') 
    def save_model(self, request, obj, form, change):
        #   CHECK IF STUDENT HAS MORE THAN MAXIMUM FREE (ONE) PAYMENTS
        exam = obj.registration.exam
        event = exam.event
        student = obj.registration.student
        registrations = student.registrations.all() # ALL REGISTRATIONS OF THE STUDENT
        current_registrations = registrations.filter(exam__in=event.exams.all())
        current_payments = Payment.objects.filter(registration__in=current_registrations)
        current_payment_count = current_payments.count()

        #   CURRENT FREE PAYMENTS MEANS PAYMENTS THAT ARE BOTH FREE AND COMPLETED 
        current_free_payments = current_payments.filter(free=True).filter(complete=True)


        def already_saved():
            val = current_free_payments.filter(registration=obj.registration).exists()
            #print("VAL :", val)
            return val

        if current_free_payments.count() >= settings.MAXIMUM_FREE_PAYMENTS and obj.free and not already_saved():
            messages.set_level(request, messages.ERROR)
            messages.error(request, "You only have one free payment")
            #print("You only have one free payment")
        else:
            obj.registration.paid = True
            obj.registration.save()
            obj.save()


#   SCHOOL
@admin.register(School)
class SchoolAdmin(ImportExportModelAdmin):
    list_display = ('name', 'student_count')
    #list_filter = ('state',)
    search_fields = ('name',)

#   STUDENT
@admin.register(Student)
class StudentAdmin(ImportExportModelAdmin):
    list_display = ('id', 'full_name','written_count','paid_count', 'checked_count','teacher_phone', 'school', 'parent_phone', 'join_date')
    list_filter = ('level',)
    search_fields = ('account__first_name', 'account__last_name', 'account__username', 'school__name')
    search_help_text = "Search by student or school name" 
    def parent_phone(self, obj):
        return mark_safe("<a href='tel:{}'>{}</a>".format(obj.account.profile.guardian_phone_number, obj.account.profile.guardian_phone_number))

    def teacher_phone(self, obj):
        teacher_ = obj.teacher_number
        return mark_safe("<a href='tel:{}'>{}</a>".format(teacher_, teacher_))


#   LEVEL
admin.site.register(Level)


#   SUBJECT
@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = ('name', 'category')
    list_filter = ('category', 'name')
    search_fields = ('name',)

#   CHOICESET
admin.site.register(ChoiceSet)


#   EVENT
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ('title', 'starts_on', 'ends_on', 'total_payment')
    #list_filter = ('year',)


#   STUDENT EXAM QUESTION
@admin.register(StudentExamQuestion)
class StudentExamQuestionAdmin(ImportExportModelAdmin):
    list_display = ('student', 'subject', 'question_number')
    list_filter = ('subject',)
    search_fields = ('student__account__first_name', 'student__account__last_name', 'student__account__username')
#    admin_caching_enabled = True
#    admin_caching_timeout_seconds = 60*10


#   STUDENT EXAM PAPER
#@admin.register(StudentExamPaper)
class StudentExamPaperAdmin(ImportExportModelAdmin):
    list_display = ('student', 'exam','submission_time')
    list_filter = ('exam', 'student')
    search_fields = ('student__account__first_name','student__account__last_name', 'student__account__username')

@admin.register(StudentReport)
class StudentReport(admin.ModelAdmin):
    list_display = ('event', 'student', 'average', 'real_average')
    list_filter = ('event',)
    search_fields = ('event__name', 'student__account__first_name', 'student__account__last_name', 'student__account__username')

