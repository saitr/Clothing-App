from apps.models import *
from apps.serializers.userserializers import *
from rest_framework import generics
from django.contrib.auth import authenticate, logout
from django.contrib.auth import get_user_model
from rest_framework import generics, status
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.views import TokenRefreshView
# from aserializers import UserSerializer
from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework.views import APIView
from rest_framework.response import Response
from django.shortcuts import render, redirect


# User = get_user_model()
# @swagger_auto_schema(tags=['SignUP'])
class SignUpView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = SignupSerializer
    # @swagger_auto_schema(operation_id='User Registration')
    @swagger_auto_schema(tags=['SignUp'])

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
    


class VerifyOtpView(generics.GenericAPIView):

    permission_classes = [AllowAny]
    @swagger_auto_schema(request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            # 'email': openapi.Schema(type=openapi.TYPE_STRING),
            'otp': openapi.Schema(type=openapi.TYPE_STRING)
        },),
        tags=['Confirm Registration']
    )

    def post(self, request,email):
        user = User.objects.filter(email=email).first()
        otp = request.data.get('otp')

        if otp == user.otp:
            user.is_active = True
            user.is_verified = True
            user.is_logged_in = True
            refresh = RefreshToken.for_user(user)
            user.jwt_token = RefreshToken.for_user(user)
            user.save()

            ############# To send the email after verification #################

            subject = 'Welcome To The Family'
            from_email = settings.DEFAULT_FROM_EMAIL
            to = [email]
            html_content = render_to_string('thankyouemail.html')
            text_content = strip_tags(html_content)
            
            msg = EmailMultiAlternatives(subject,text_content,from_email,to)
            msg.attach_alternative(html_content,'text/html')
            msg.send()

            return Response({'status':200,'refresh': str(refresh), 'access': str(refresh.access_token),'verification':'verified successfully'})
        else:
            return Response({'detail': 'Invalid otp'}, status=status.HTTP_401_UNAUTHORIZED)
        
# class SigninView(generics.GenericAPIView):
#     permission_classes = [AllowAny]
#     serializer_class = SignInSerializer

#     def post(self, request):
#         username = request.data.get('username')
#         password = request.data.get('password')

#         user = User.objects.get(username=username, password=password)
#         if user:
#             user.is_logged_in = True
#             refresh = RefreshToken.for_user(user)
#             print('this is refresh token',refresh)
#             access_token = str(refresh.access_token)
#             user.jwt_token = RefreshToken.for_user(user)
#             print('this is access token',access_token)
#             user.save()

            
#             return Response({'status':200,'refresh': str(refresh), 'access': str(refresh.access_token)})
#         else:
#             return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)

class SigninView(generics.GenericAPIView):
    permission_classes = [AllowAny]
    serializer_class = SignInSerializer
    @swagger_auto_schema(tags=['SignIn'])

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        try:
            user = User.objects.get(username=username)
            if check_password(password, user.password):
                # password matches
                user.is_logged_in = True
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                user.jwt_token = RefreshToken.for_user(user)
                user.save()
                return Response({'status':200,'refresh': str(refresh), 'access': access_token})
            else:
                # password does not match
                return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
        except User.DoesNotExist:
            # user does not exist
            return Response({'detail': 'Invalid credentials'}, status=status.HTTP_401_UNAUTHORIZED)
                    

class LogoutView(generics.GenericAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    
    @swagger_auto_schema(tags=['Logout'])
    def post(self, request):
        user = request.user
        user.is_logged_in = False
        user.jwt_token = None
        user.save()
        logout(request)
        return Response({'detail': 'Successfully logged out'})
