from rest_framework.views import APIView
from rest_framework.response import Response
from .serializers import ChangePasswordSerializer, ForgotPasswordCompleteSerializer, ForgotPaswordSerializer, \
    RegistrationSerializer, LoginSerializer, ActivationSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from .permissoins import IsActivePermission
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema


class RegistrationView(APIView):
    @swagger_auto_schema(request_body=RegistrationSerializer())
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response('Аккаунт успешно создан', status=201)


class ActivationView(APIView):
    @swagger_auto_schema(request_body=ActivationSerializer())
    def post(self, request):
        serializer = ActivationSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.activate()
        return Response('Аккаунт успешно активирован!', status=200)


class LoginView(ObtainAuthToken):
    request_body = RegistrationSerializer()
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsActivePermission]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Вы вышли со совего аккаунта')


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ChangePasswordSerializer())
    def post(self, request):
        serializer = ChangePasswordSerializer(data=request.data, context={'request': request})

        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()

        return Response('Status: 200. Пароль успешно обновлен')


class ForgotPasswordView(APIView):

    @swagger_auto_schema(request_body=ForgotPaswordSerializer())
    def post(self, request):
        serializer = ForgotPaswordSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.send_verification_email()

        return Response('Вам выслали сообщение для восстановления аккаунта')


class ForgotPasswordCompleteView(APIView):

    @swagger_auto_schema(request_body=ForgotPasswordCompleteSerializer())
    def post(self, request):
        serializer = ForgotPasswordCompleteSerializer(data=request.data)

        if serializer.is_valid(raise_exception=True):
            serializer.set_new_password()
            return Response('Пароль успешно изменён')