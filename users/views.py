from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import RegisterSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth import get_user_model
from rest_framework.exceptions import AuthenticationFailed

User = get_user_model()


class EmailLoginSerializer(TokenObtainPairSerializer):
    username_field = 'email'   # 🔥 IMPORTANT

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")

        # 🔍 Find user by email
        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid email or password")

        # 🔐 Check password
        if not user.check_password(password):
            raise AuthenticationFailed("Invalid email or password")

        # ❗ Check active
        if not user.is_active:
            raise AuthenticationFailed("User is inactive")

        # 🎯 Generate token
        data = super().validate({
            "email": email,
            "password": password
        })

        return data


class EmailLoginView(TokenObtainPairView):
    serializer_class = EmailLoginSerializer


@api_view(['POST'])
def register(request):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
        serializer.save()
        return Response({"message": "User registered successfully"})

    return Response(serializer.errors)