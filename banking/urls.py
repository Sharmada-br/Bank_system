from django.urls import path
from banking.views import home  
from .views import create_account, home, my_accounts, deposit, transaction_history, withdraw, delete_account

urlpatterns = [
    path('', home),  
    path('create/', create_account),
    path('my-accounts/', my_accounts),
    path('deposit/', deposit),
    path('withdraw/', withdraw),
    path('delete/', delete_account),
    path('transactions/', transaction_history),
]