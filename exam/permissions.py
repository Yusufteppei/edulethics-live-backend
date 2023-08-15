from rest_framework.permissions import BasePermission, SAFE_METHODS

from .models import Student, Registration, Level, Subject, Event, Exam

#   THIS IS UNIQUELY ATTACHED TO AN EXAM
#   SO IF A STUDENT HAS PAID FOR AN EXAM, HE HAS ACCESS TO THE RESOURCE THAT HAS THAT EXAM ATTACHED TO IT
class IsPaid(BasePermission):
    
    def has_object_permission(self, request, view, obj):
        if request.method in SAFE_METHODS:
            user = request.user
            student = Student.objects.get(account=user)

            level_name = student.level.name
            level = Level.objects.get(name=level_name)
            #subject_name = request.query_params.get('subject')
            #subject = Subject.objects.get(name=subject_name)
            for i in Event.objects.all():
                if i.active:
                    event = i.id
                    print(event)
            exam = Exam.objects.get(level=level, subject=obj.subject, event=event)
            #print("Exam : ", exam)
            registration = Registration.objects.get(student=student, exam=exam)
            #print(registration.paid)
            if registration.paid == True:
                return True
            return False
        return False
        

class IsOwner(BasePermission):

    def has_object_permission(self, request, view, obj):
        if request.user == obj.owner:
            return True
        return False
