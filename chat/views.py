from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet
from .models import *
from rest_framework.decorators import api_view
# Create your views here.
from django.http import JsonResponse

class ChatViewSet(ModelViewSet):

    def get_queryset(self):
        q = Chat.objects.filter( Q(person1= obj) | Q(person2=obj) )
        return q


class MessageViewSet(ModelViewSet):

    def get_queryset(self):
        q = Message.objects.all()


def get_student_by_username(username):
    account = UserAccount.objects.get(username=username)
    return Student.objects.get(account=account)


@api_view(['POST', 'GET'])
def message(request):

    if request.method == 'POST':
        sender = Student.objects.get(account=request.user)
        receiver = Student.objects.get(id=request.data['receiver'])
        message = request.data['message']
        
        response = {"message": "Message sent"}

        if Chat.objects.filter(person1=sender, person2=receiver).exists():
            chat = Chat.objects.get(person1=sender, person2=receiver)
        elif Chat.objects.filter(person2=sender, person1=receiver).exists():
            chat = Chat.objects.get(person2=sender, person1=receiver)
        else:
            chat = Chat.objects.create(person2=sender, person1=receiver)
            response = {"message": "Chat created. Message sent"}


        Message.objects.create(chat=chat, message=message, sender=sender)
        
        return JsonResponse(response)

    
    elif request.method == 'GET':
        sender = Student.objects.get(account=request.user)
        receiver = get_student_by_username(request.query_params.get('receiver'))
        
        if Chat.objects.filter(person1=sender, person2=receiver).exists():
            chat = Chat.objects.get(person1=sender, person2=receiver)
        elif Chat.objects.filter(person2=sender, person1=receiver).exists():
            chat = Chat.objects.get(person2=sender, person1=receiver)
        else:
            chat = Chat.objects.create(person2=sender, person1=receiver)

        messages = Message.objects.filter(chat=chat)
        messages_ = []

        for i in messages:
            if i.sender == sender:
                is_user = True
            else:
                is_user = False
            text = i.message
            messages_.append({"isUser":  is_user, "text": text})
        return JsonResponse(messages_, safe=False)

def get_student_by_username(username):
    account = UserAccount.objects.get(username=username)
    return Student.objects.get(account=account)


@api_view(['POST', 'GET'])
def chat(request):
    
    person1 = Student.objects.get(account=request.user)
    person2 = get_student_by_username(request.data['person2'])


    if request.method == 'POST':
        pass

