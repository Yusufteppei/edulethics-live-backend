from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *
from .admin_views import *

router = DefaultRouter()

#router.register('events', EventViewSet, basename='event')
#router.register('students', StudentViewSet, basename='student')
router.register('subjects', SubjectViewSet, basename='subject')
#router.register('schools', SchoolViewSet, basename='school')
router.register('levels', LevelViewSet, basename='level')
#router.register('choicesets', ChoicesetViewSet, basename='choiceset')
#router.register('questions', QuestionViewSet, basename='question')
router.register('exams', ExamViewSet, basename='exam')
router.register('exam-questions', ExamQuestionViewSet, basename='exam-question')
router.register('student-exam-questions', StudentExamQuestionViewSet, basename='student-exam-question')
#router.register('student-exam-papers', StudentExamPaperViewSet, basename='student-exam-paper')
#router.register('registrations', RegistrationViewSet, basename='registration')
#router.register('payments', PaymentViewSet, basename='payment')


urlpatterns = [
    path('', include(router.urls)),
    path('school-count/', school_count, name='school-count'),
    path('student-count/', student_count, name='student-count'),
    path('student/', student, name='student'),
    path('school/', school, name='school_'),
    path('username-available/', check_username_availability, name='username-available'),
    path('summernote/', include('django_summernote.urls')),
    path('get-pins/', get_pins, name='get-pins'),
    path('pay-with-pin/', pay_with_pin, name='pay-with-pin'),
    path('pay-free/', pay_free, name='pay-free'),
    path('pay-with-paystack/', pay_with_paystack, name='pay-with-paystack'),
    path('submit-answers/', submit_answers, name='submit-answers'),
    path('taken-exams/', taken_exams, name='taken-exams'),
    path('paid-exams/', paid_exams, name='paid-exams'),
    path('is-taken/', is_taken, name='is-taken'),
    path('has-written-all/', has_written_all, name='has-written-all'),
    path('has-used-free-payment/', has_used_free_payment, name='has-used-free-payment'),
    path('register/', register, name='register'),
    path('get-top-students-per-exam/', get_top_students_per_exam, name='get-top-students-per-exam'),
    path('has-made-real-payment/', has_made_real_payment, name='has-made-real-payment'),
    path('exam-count/', exam_count, name='exam-count'),
    path('unpaid-exams/', unpaid_exams, name='unpaid-exam'),
    path('events/', events, name='events'),
    path('event/', event, name='event'),
    path('check-result/', check_result, name='check-result'),
    path('reset-password/', reset_password, name='reset-password')
]

####        ANALYTICS URLS    ####
urlpatterns += [
    path('student-file/', student_file, name='student-file'),
    path('student-data/', student_data, name='student-data')
]
