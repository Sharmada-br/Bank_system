from django.urls import path
from .views import EmailLoginView, register

urlpatterns = [
    path('register/', register),
    path('login/', EmailLoginView.as_view()),
]