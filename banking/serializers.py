from rest_framework import serializers
from .models import Account


class AccountSerializer(serializers.ModelSerializer):

    class Meta:
        model = Account

        fields = [
            'id',
            'bank_name',
            'account_number',
            'ifsc_code',
            'account_type',
            'balance'
        ]