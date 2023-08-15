from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import UserAccount, Profile
from .serializers import ProfileSerializer
from exam.permissions import IsOwner
from rest_framework.permissions import IsAdminUser, SAFE_METHODS, AllowAny, IsAuthenticated
from rest_framework.decorators import api_view
from django.http import JsonResponse
from exam.models import *


from django.contrib.auth.hashers import make_password, check_password

# Create your views here.


class ProfileViewSet(ModelViewSet):
    serializer_class = ProfileSerializer
    permission_classes = [ AllowAny, ]
    def get_queryset(self):
        username = self.request.query_params.get('username')
        owner = UserAccount.objects.get(username=username)
        profile = Profile.objects.get(owner=owner)
        return profile

#    def get_permissions(self):
#        if self.request.method in SAFE_METHODS or self.request.method == 'PATCH':
#            return (IsAdminUser(), )



#   RETURNS A BOOLEAN
@api_view(['POST', 'GET'])
def username_available(request):
    username = request.query_params.get('username')

    if UserAccount.objects.filter(username=username).exists():
        #print("Username exists already")
        return JsonResponse ({
            'available': False
        })
    else:
        #print("Username is available")
        return JsonResponse ({
            'available': True
        })


#   RETURNS A BOOLEAN
@api_view(['POST', 'GET'])
def email_available(request):
    email = request.query_params.get('email')

    if UserAccount.objects.filter(email=email).exists():
        print("User with email exists already")
        return JsonResponse ({
            'available': False
        })
    else:
        #print("Email is available")
        return JsonResponse ({
            'available': True
        })

@api_view(['POST'])
def signup(request):
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    username = request.data['username']
    level = request.data['level']
    state = request.data['state']
    dob = request.data['dob']
    password = request.data['password']
    school = request.data['school'].upper()
    email = request.data['email']
    teacher_number = request.data['teacher_number']
    school_type = request.data['school_type']
    guardian_number = request.data['guardian_number']
    school_address = request.data['school_address']
    guardian_first_name = request.data['guardian_first_name']
    guardian_last_name = request.data['guardian_last_name']
    guardian_email = request.data['guardian_email']
    guardian_phone_number = request.data['guardian_number']
    school = School.objects.get_or_create(name=school)
    if not school[1]:
        school = school[0]
    else:
        school = school[0]
        school.school_type = school_type
        school.address = school_address
        school.save()
    level = Level.objects.get(name=level)

    user = UserAccount.objects.create_user(first_name=first_name, last_name=last_name, username=username,password=password, email=email)
    Profile.objects.create(owner=user, phone_number=guardian_number, guardian_first_name=guardian_first_name, guardian_last_name=guardian_last_name, guardian_phone_number=guardian_phone_number, guardian_email=guardian_email)
    student = Student.objects.create(account=user, state=state, teacher_number=teacher_number, level=level, school=school)
    return JsonResponse({"message": "Account created successfully"})


@api_view(['POST'])
def change_password_with_username(request):
    user = UserAccount.objects.get(username=request.data['username'].lower())
    new_password = request.data['new_password']
    
    user.password = make_password(new_password)
    user.save()
    return JsonResponse({"message": f"{user.username} new password is {new_password}"})


@api_view(['POST'])
def change_password_with_full_name(request):
    first_name = request.data['first_name']
    last_name = request.data['last_name']
    
    user = UserAccount.objects.get(first_name = first_name, last_name=last_name)
    
    new_password = request.data['new_password']

    user.password = make_password(new_password)
    user.save()

def change_password(request):
    pass
