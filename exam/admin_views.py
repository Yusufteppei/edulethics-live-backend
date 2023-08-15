from .models import *
from django.shortcuts import render
from rest_framework.decorators import api_view
from django.http import FileResponse, JsonResponse

def menu(request):
    context = {}
    return render(request, 'exam/index.html', context)



def student_(student):
    school_type = 'unnamed'
    try:
        full_name = student.full_name
        school = student.school.name
        written_count = student.written_count
        checked_count = student.checked_count
        paid_count = student.paid_count
        parent_no = student.parent_number
        state = student.state
        school_type = student.school.school_type
        teacher_no = student.teacher_number
        join_date = student.join_date



    except:
        pass

    return f"{full_name}, {school.replace(',', ' ')}, {school_type}, {written_count}, {checked_count}, {paid_count}, {parent_no}, {state}, {teacher_no}, {join_date}\n"
def create_csv(students):
    with open('datasets/students.csv', 'w') as f:
        f.write(',Name, School, School Type, Written Count, Checked Count, Paid Count, Parent no, State, Teacher no, Join Date\n')
        for student in students:
            #print(student.full_name)
            f.write(student_(student))

## DELETE STUDENT WITHOUT SCHOOL
## Student.objects.filter(school=None).delete()
#s = Student.objects.all()
#create_csv(s)


##  ANALYTICS ENDPOINT  ##

@api_view(['GET'])
def student_file(request):
    create_csv(Student.objects.all())
    return FileResponse(open('datasets/students.csv', 'rb'))

