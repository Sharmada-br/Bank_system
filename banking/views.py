from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.http import HttpResponse
from decimal import Decimal
import random

from .models import Account, Transaction


def home(request):
    return HttpResponse("Bank System Running 🚀")


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_account(request):
    account_number = str(random.randint(10000000, 99999999))

    account = Account.objects.create(
        user=request.user,
        account_number=account_number,
        bank_name=request.data.get('bank_name'),
        account_type=request.data.get('account_type')
    )

    return Response({
        "message": "Account created successfully",
        "account_number": account.account_number
    })


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


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request):
    account = get_object_or_404(
        Account,
        account_number=request.data.get('account_number').strip(),
        user=request.user
    )

    amount = Decimal(request.data.get('amount'))
    account.balance += amount
    account.save()

    Transaction.objects.create(
        account=account,
        amount=amount,
        transaction_type='deposit'
    )

    return Response({
        "message": "Amount deposited",
        "balance": account.balance
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    account = get_object_or_404(
        Account,
        account_number=request.data.get('account_number').strip(),
        user=request.user
    )

    amount = Decimal(request.data.get('amount'))

    if account.balance < amount:
        return Response({"error": "Insufficient balance"}, status=400)

    account.balance -= amount
    account.save()

    Transaction.objects.create(
        account=account,
        amount=amount,
        transaction_type='withdraw'
    )

    return Response({
        "message": "Amount withdrawn",
        "balance": account.balance
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    account_number = request.GET.get('account_number')

    account = get_object_or_404(
        Account,
        account_number=account_number.strip(),
        user=request.user
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

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    account = get_object_or_404(
        Account,
        account_number=request.data.get('account_number').strip(),
        user=request.user
    )

    account.delete()

    return Response({"message": "Account deleted successfully"})