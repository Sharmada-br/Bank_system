from django.urls import path
from .views import add_todo, get_message, get_todos, get_messages, delete_todo
from banking.views import (

    home,
    create_account,
    my_accounts,
    account_details,
    update_account,
    deposit,
    withdraw,
    transfer_money,
    delete_account,
    transaction_history,

    account_page,
    login_page,

    register_page,
    dashboard_page,
    accounts_page,
    add_account_page,
    edit_account_page,
    summary_page,
    transfer_page,
    transactions_page
)

urlpatterns = [

    path('', register_page),
    path('login-page/', login_page),
    path('message/', get_message),
    path('message/<int:count>/', get_messages),
    path('todos/', get_todos),
    path('account-page/', account_page),
    path('add-todo/', add_todo),
    path('delete-todo/<int:id>/', delete_todo),
    path('register-page/', register_page),

    path('dashboard/', dashboard_page),

    path('accounts/', accounts_page),

    path('add-account/', add_account_page),

    path('edit-account/', edit_account_page),

    path('summary/', summary_page),

    path('transfer/', transfer_page),

    path('transactions-page/', transactions_page),

    path('account-details/', account_page),

    path('create/', create_account),

    path('my-accounts/', my_accounts),

    path('deposit/', deposit),

    path('withdraw/', withdraw),

    path('transfer-money/', transfer_money),

    path('delete/', delete_account),

    path('transactions/', transaction_history),

     path(
        'account/<int:id>/',
        account_details,
        name='account_details'
    ),
 

    path(
        'account/<int:id>/update/',
        update_account,
        name='update_account'
    ),
]
