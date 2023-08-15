from .models import *
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import check_password, make_password



def index(request):
    template = ''
    context = {}
    return render(request, template, context)


def change_password(request):
    username = request.cleaned_data['username']

    if request.method == 'POST' and request.user.is_staff:
        new_password = request.cleaned_data['password']

        user = UserAccount.objects.get(username=username)
        user.password = make_password(new_password)
        user.save()

    #   RECORD REQUESTER
    with open('password_changes', 'a') as f:
        f.write(f'{request.user}, {username}')
        f.close()
    template = '' 
    context = {
        'message': f'Password changed to {user.password}'
    }
    return render(request, template, context}
