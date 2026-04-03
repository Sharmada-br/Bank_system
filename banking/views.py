from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Account, Transaction
import random
from decimal import Decimal

# Home
from django.http import HttpResponse
def home(request):
    return HttpResponse("Bank System Running 🚀")


# Create Account
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_account(request):
    account_number = str(random.randint(10000000, 99999999))

    account = Account.objects.create(
        user=request.user,
        account_number=account_number,
        bank_name=request.data['bank_name'],
        account_type=request.data['account_type']
    )

    return Response({"account_number": account.account_number})


# My Accounts
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_accounts(request):
    accounts = Account.objects.filter(user=request.user)

    data = []
    for acc in accounts:
        data.append({
            "account_number": acc.account_number,
            "bank_name": acc.bank_name,
            "account_type": acc.account_type,
            "balance": acc.balance
        })

    return Response(data)


# Deposit
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request):
    account = Account.objects.get(account_number=request.data['account_number'])
    amount = Decimal(request.data['amount'])
    account.balance += amount
    account.save()

    Transaction.objects.create(account=account, amount=amount, transaction_type='deposit')

    return Response({"balance": account.balance})


# Withdraw
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    account = Account.objects.get(account_number=request.data['account_number'])
    amount = Decimal(request.data['amount'])
    if account.balance < amount:
        return Response({"error": "Insufficient balance"})

    account.balance -= amount
    account.save()

    Transaction.objects.create(account=account, amount=amount, transaction_type='withdraw')

    return Response({"balance": account.balance})


# Delete Account
@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    account = Account.objects.get(account_number=request.data['account_number'])
    account.delete()
    return Response({"message": "Account deleted"})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    account_number = request.GET.get('account_number')

    account = Account.objects.get(
        account_number=account_number,
        user=request.user   # 🔐 security
    )

    transactions = Transaction.objects.filter(account=account)

    data = []
    for t in transactions:
        data.append({
            "amount": t.amount,
            "type": t.transaction_type,
            "date": t.created_at
        })

    return Response(data)