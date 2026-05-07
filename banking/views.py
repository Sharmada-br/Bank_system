from rest_framework.decorators import (
    api_view,
    permission_classes
)

from rest_framework.permissions import (
    IsAuthenticated
)

from rest_framework.response import Response

from django.shortcuts import (
    get_object_or_404,
    render
)

from django.http import HttpResponse

from decimal import Decimal

import random

from .models import (
    Account,
    Transaction
)


def home(request):

    return HttpResponse(
        "Bank System Running 🚀"
    )


# CREATE ACCOUNT

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def create_account(request):

    account_number = str(
        random.randint(10000000, 99999999)
    )

    balance = request.data.get(
        'balance',
        0
    ) or 0

    account = Account.objects.create(

        user=request.user,

        account_number=account_number,

        bank_name=request.data.get(
            'bank_name'
        ),

        account_type=request.data.get(
            'account_type'
        ),

        balance=Decimal(
            str(balance).replace(
                '₹',
                ''
            ).replace(
                ',',
                ''
            ).strip()
        )
    )

    return Response({

        "message":
            "Account created successfully",

        "account_number":
            account.account_number
    })


# MY ACCOUNTS

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def my_accounts(request):

    accounts = Account.objects.filter(
        user=request.user
    )

    data = []

    for acc in accounts:

        data.append({

            "id": acc.id,

            "account_number":
                acc.account_number,

            "bank_name":
                acc.bank_name,

            "account_type":
                acc.account_type,

            "balance":
                acc.balance
        })

    return Response(data)


# ACCOUNT DETAILS BY ID

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def account_details(request, id):

    account = get_object_or_404(

        Account,

        id=id,

        user=request.user
    )

    transactions = Transaction.objects.filter(
        account=account
    )

    data = {

        "id": account.id,

        "account_number":
            account.account_number,

        "bank_name":
            account.bank_name,

        "account_type":
            account.account_type,

        "balance":
            account.balance,

        "transactions": [

            {
                "amount": t.amount,
                "type": t.transaction_type,
                "date": t.created_at
            }

            for t in transactions
        ]
    }

    return Response(data)


# DEPOSIT

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def deposit(request):

    account = get_object_or_404(

        Account,

        account_number=request.data.get(
            'account_number'
        ).strip(),

        user=request.user
    )

    amount = Decimal(
        request.data.get('amount')
    )

    account.balance += amount

    account.save()

    Transaction.objects.create(

        account=account,

        amount=amount,

        transaction_type='deposit'
    )

    return Response({

        "message":
            "Amount deposited",

        "balance":
            account.balance
    })


# WITHDRAW

@api_view(['POST'])
@permission_classes([IsAuthenticated])

def withdraw(request):

    account = get_object_or_404(

        Account,

        account_number=request.data.get(
            'account_number'
        ).strip(),

        user=request.user
    )

    amount = Decimal(
        request.data.get('amount')
    )

    if account.balance < amount:

        return Response(
            {
                "error":
                    "Insufficient balance"
            },
            status=400
        )

    account.balance -= amount

    account.save()

    Transaction.objects.create(

        account=account,

        amount=amount,

        transaction_type='withdraw'
    )

    return Response({

        "message":
            "Amount withdrawn",

        "balance":
            account.balance
    })


# TRANSACTION HISTORY

@api_view(['GET'])
@permission_classes([IsAuthenticated])

def transaction_history(request):

    account_number = request.GET.get(
        'account_number'
    )

    account = get_object_or_404(

        Account,

        account_number=account_number.strip(),

        user=request.user
    )

    transactions = Transaction.objects.filter(
        account=account
    )

    data = []

    for t in transactions:

        data.append({

            "amount": t.amount,

            "type": t.transaction_type,

            "date": t.created_at
        })

    return Response(data)


# DELETE ACCOUNT

@api_view(['DELETE'])
@permission_classes([IsAuthenticated])

def delete_account(request):

    account = get_object_or_404(

        Account,

        account_number=request.data.get(
            'account_number'
        ).strip(),

        user=request.user
    )

    account.delete()

    return Response({

        "message":
            "Account deleted successfully"
    })


# TEMPLATE PAGES

def account_page(request):

    return render(
        request,
        'account details.html'
    )


def login_page(request):

    return render(
        request,
        'login.html'
    )


def register_page(request):

    return render(
        request,
        'register.html'
    )


def dashboard_page(request):

    return render(
        request,
        'dashboard.html'
    )


def accounts_page(request):

    return render(
        request,
        'accounts.html'
    )


def add_account_page(request):

    return render(
        request,
        'add_account.html'
    )


def edit_account_page(request):

    return render(
        request,
        'Editaccount.html'
    )


def summary_page(request):

    return render(
        request,
        'summary.html'
    )


def transfer_page(request):

    return render(
        request,
        'transfer.html'
    )


def transactions_page(request):

    return render(
        request,
        'transactions.html'
    )
