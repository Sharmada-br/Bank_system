from rest_framework import serializers
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email', 'password', 'phone']
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data['email'],
            password=validated_data['password'],
            phone=validated_data['phone']
        )
        return user
    
    def validate_email(self, value):

        if User.objects.filter(email=value).exists():

            raise serializers.ValidationError(
            "Account already exists"
        )

        return value