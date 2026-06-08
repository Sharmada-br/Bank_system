from decimal import Decimal, InvalidOperation
import random

from django.db import transaction as db_transaction
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import AccountSerializer
from .models import Todo


from .models import Account, Transaction


def parse_money(value):
    if value in (None, ''):
        return Decimal('0')

    cleaned = (
        str(value)
        .replace('₹', '')
        .replace('â‚¹', '')
        .replace(',', '')
        .strip()
    )

    return Decimal(cleaned or '0')


def serialize_account(account):
    return {
        'id': account.id,
        'account_number': account.account_number,
        'bank_name': account.bank_name,
        'account_type': account.account_type,
        'balance': account.balance,
        'ifsc_code': account.ifsc_code,
    }


def home(request):
    return HttpResponse('Bank System Running')


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def create_account(request):
    account_number = str(random.randint(10000000, 99999999))

    while Account.objects.filter(account_number=account_number).exists():
        account_number = str(random.randint(10000000, 99999999))

    account = Account.objects.create(

    user=request.user,

    account_number=account_number,

    bank_name=request.data.get(
        'bank_name'
    ) or 'Aureon Bank',

    ifsc_code=request.data.get(
        'ifsc_code'
    ) or 'AUREON0001',

    account_type=request.data.get(
        'account_type'
    ) or 'Savings',

    balance=parse_money(
        request.data.get('balance', 0)
    ),
)

    return Response({
        'message': 'Account created successfully',
        **serialize_account(account),
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def my_accounts(request):
    accounts = Account.objects.filter(user=request.user).order_by('id')
    return Response([serialize_account(account) for account in accounts])



    return Response(data)
@api_view(['GET'])
def account_details(request, id):

    account = get_object_or_404(Account, id=id)

    transactions = Transaction.objects.filter(
        account=account
    ).order_by('-created_at')

    running_balance = float(account.balance)

    transactions_data = []

    for transaction in transactions:

        transactions_data.append({

            'id': transaction.id,

            'amount': float(transaction.amount),

            'type': transaction.transaction_type,

            'date': transaction.created_at,

            'balance': float(running_balance)
        })

        if transaction.transaction_type == 'deposit':

            running_balance -= float(transaction.amount)

        else:

            running_balance += float(transaction.amount)

    return Response({

        'id': account.id,

        'account_number': account.account_number,

        'bank_name': account.bank_name,

        'account_type': account.account_type,

        'balance': float(account.balance),

        'ifsc_code': account.ifsc_code,

        'transactions': transactions_data
    })

@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
def update_account(request, id):
    account = get_object_or_404(Account, id=id)

    if request.data.get('bank_name'):
        account.bank_name = request.data.get('bank_name')

    if request.data.get('account_type'):
        account.account_type = request.data.get('account_type')

    if request.data.get('balance') not in (None, ''):
        account.balance = parse_money(request.data.get('balance'))

    account.save()

    return Response({
        'message': 'Account updated successfully',
        **serialize_account(account),
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request):
    account = get_object_or_404(
        Account,
        account_number=str(request.data.get('account_number') or '').strip(),
        user=request.user,
    )

    amount = parse_money(request.data.get('amount'))

    if amount <= 0:
        return Response({'error': 'Amount must be greater than zero'}, status=400)

    account.balance += amount
    account.save()

    Transaction.objects.create(
        account=account,
        amount=amount,
        transaction_type='deposit',
    )

    return Response({
        'message': 'Amount deposited',
        'balance': account.balance,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    account = get_object_or_404(
        Account,
        account_number=str(request.data.get('account_number') or '').strip(),
        user=request.user,
    )

    amount = parse_money(request.data.get('amount'))

    if amount <= 0:
        return Response({'error': 'Amount must be greater than zero'}, status=400)

    if account.balance < amount:
        return Response({'error': 'Insufficient balance'}, status=400)

    account.balance -= amount
    account.save()

    Transaction.objects.create(
        account=account,
        amount=amount,
        transaction_type='withdraw',
    )

    return Response({
        'message': 'Amount withdrawn',
        'balance': account.balance,
    })


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def transfer_money(request):
    from_account_number = str(request.data.get('from_account') or '').strip()
    to_account_number = str(request.data.get('to_account') or '').strip()
    raw_amount = request.data.get('amount')

    if not from_account_number:
        return Response({'error': 'Please select valid account details'}, status=400)

    if not to_account_number:
        return Response({'error': 'Please select valid account details'}, status=400)

    if raw_amount in (None, ''):
        return Response({'error': 'Please select valid account details'}, status=400)

    if from_account_number == to_account_number:
        return Response({'error': 'Choose a different destination account'}, status=400)

    try:
        from_account = Account.objects.get(
            account_number=from_account_number,
            user=request.user,
        )
        to_account = Account.objects.get(
            account_number=to_account_number,
            user=request.user,
        )
    except Account.DoesNotExist:
        return Response({'error': 'No Account Found'}, status=404)

    try:
        amount = parse_money(raw_amount)
    except (InvalidOperation, ValueError):
        return Response({'error': 'Please select valid account details'}, status=400)

    if amount <= 0:
        return Response({'error': 'Please select valid account details'}, status=400)

    if from_account.id == to_account.id:
        return Response({'error': 'Choose a different destination account'}, status=400)

    if from_account.balance < amount:
        return Response({'error': 'Insufficient balance'}, status=400)

    with db_transaction.atomic():
        from_account.balance -= amount
        to_account.balance += amount
        from_account.save()
        to_account.save()

        Transaction.objects.create(
            account=from_account,
            amount=amount,
            transaction_type='withdraw',
        )
        Transaction.objects.create(
            account=to_account,
            amount=amount,
            transaction_type='deposit',
        )

    return Response({
        'message': 'Transfer completed successfully',
        'from_balance': from_account.balance,
        'to_balance': to_account.balance,
    })


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def transaction_history(request):
    account = get_object_or_404(
        Account,
        account_number=str(request.GET.get('account_number') or '').strip(),
        user=request.user,
    )
    transactions = Transaction.objects.filter(account=account).order_by('-created_at')

    return Response([
        {
            'id': transaction.id,
            'amount': transaction.amount,
            'type': transaction.transaction_type,
            'date': transaction.created_at,
        }
        for transaction in transactions
    ])


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_account(request):
    account = get_object_or_404(
        Account,
        account_number=str(request.data.get('account_number') or '').strip(),
        user=request.user,
    )
    account.delete()

    return Response({'message': 'Account deleted successfully'})

@api_view(['PUT'])
def update_todo(request, id):

    todo = Todo.objects.get(id=id)

    todo.text = request.data.get(
        'text',
        todo.text
    )

    todo.completed = request.data.get(
        'completed',
        todo.completed
    )

    todo.due_date = request.data.get(
    'due_date',
    todo.due_date
)
    todo.save()

    return Response({
        "id": todo.id,
        "text": todo.text,
        "completed": todo.completed,
        "due_date": todo.due_date,

        "created_at": todo.created_at
    })


def account_page(request):
    return render(request, 'account details.html')


def login_page(request):
    return render(request, 'login.html')


def register_page(request):
    return render(request, 'register.html')


def dashboard_page(request):
    return render(request, 'dashboard.html')


def accounts_page(request):
    return render(request, 'accounts.html')


def add_account_page(request):
    return render(request, 'add_account.html')


def edit_account_page(request):
    return render(request, 'Editaccount.html')


def summary_page(request):
    return render(request, 'summary.html')


def transfer_page(request):
    return render(request, 'transfer.html')


def transactions_page(request):
    return render(request, 'transactions.html')

@api_view(['GET'])
def get_message(request):
    return Response({
        "message": "Hello from Django Backend"
    })

@api_view(['GET'])
def get_todos(request):
    todos = Todo.objects.all()

    data = []

    for todo in todos:
        data.append({
            "id": todo.id,
            "text": todo.text,
            "completed": todo.completed,
            "due_date": todo.due_date,
            "created_at": todo.created_at

        })

    return Response(data)
@api_view(['POST'])
def add_todo(request):
    print("Received Data:", request.data)
    added_todo = Todo.objects.create(
        text=request.data.get('text'),
        completed=False,
        due_date=request.data.get('due_date')
    )

    return Response({
        'id': added_todo.id,
        'text': added_todo.text,
        'completed': added_todo.completed,
        'due_date': added_todo.due_date,
        'created_at': added_todo.created_at
    })

@api_view(['GET'])
def get_messages(request, count):
    data = []

    for i in range(count):
        data.append(f"React Developer Tools {i + 1}")

    return Response(data)

@api_view(['DELETE'])
def delete_todo(request, id):
    todo = Todo.objects.get(id=id)
    todo.delete()

    return Response({
        "message": "Todo deleted successfully"
    })