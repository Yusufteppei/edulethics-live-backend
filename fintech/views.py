from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import BankAccount

@api_view(['GET'])
def activate_account(request):
    account = request.user
    
    bank_account = BankAccount.objects.get_or_create(user_account=account)[0]
    bank_account.activate()
