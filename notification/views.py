from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import *
from exam.models import Student
# Create your views here.

@api_view(['GET'])
def broadcasts(request):
    student = Student.objects.get(account=request.user)
    level = student.level

    broadcasts = level.broadcast_set.all()
    
    broadcasts_ = []

    for j in broadcasts:
        if student.checked_count >= j.result_check_requirement and student.written_count >= j.exam_write_requirement:
            broadcasts_.append(j)
    response = []

    for i in broadcasts_:
        x = {'id': i.id, 'topic': i.topic, 'message': i.message, 'category': i.category, 'time': i.time}
        response.append(x)

    return JsonResponse(response, safe=False)


@api_view(['GET'])
def has_viewed_all_broadcasts(request):
    student = Student.objects.get(account=request.user)

    for i in Broadcast.objects.all():
        i.viewed_students.add(student)

    return JsonResponse({'message': 'done'})

