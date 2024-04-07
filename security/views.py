from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.serializers import TokenVerifySerializer
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from rest_framework_simplejwt.tokens import AccessToken
from django.contrib.auth.models import User
import re
from django.conf import settings
from django.utils.text import capfirst
from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from rest_framework.permissions import AllowAny
from .models import Client

# Vista para autenticar usuarios y generar tokens
class UserLoginView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        username = request.data.get('username', None)
        password = request.data.get('password', None)

        # Validación de campos requeridos
        errors = {}
        if username is None:
            errors["username"] = "Campo requerido"
        if password is None:
            errors["password"] = "Campo requerido"

        # Manejo de errores de validación
        if len(errors.keys()) > 0:
            return Response({"detail": errors}, status=status.HTTP_400_BAD_REQUEST)

        # Autenticar al usuario
        user = authenticate(username=username, password=password)
        if user is None:
            return Response({"detail": "El usuario o contraseña son incorrectos"}, status=status.HTTP_401_UNAUTHORIZED)

        try:
            # Generar tokens de acceso y actualización
            refresh = RefreshToken.for_user(user)
            # model_employee = None
            # if not username == 'system':
            #     model_employee = Employee.objects.select_related('user','job').get(document_number=username)
            #     if user.groups.first().id == 1: # Admin
            #         rol = 'ADM'
            #     elif user.groups.first().id == 2: # User
            #         rol = 'USU'
            #     elif user.groups.first().id == 3: # Supervisor
            #         rol = 'SUP'
            #     elif user.groups.first().id == 4: # Recursos Humanos
            #         rol = 'RHH'
            

            # if model_employee:
            #     user_info = {
            #         'id': model_employee.id if model_employee.id else "",
            #         'job_id': model_employee.job.id if model_employee.job.id else '',
            #         'job': model_employee.job.name if model_employee.job.name else '',
            #         'name': model_employee.complete_name(),
            #         'sede': model_employee.sede.name if model_employee.sede.name else '',
            #         'company': model_employee.company.business_name if model_employee.company.business_name else '',
            #         'username': user.username,
            #         'rol': rol if rol else ''
            #     }
            # else:
            #     user_info = {
            #         'name': user.first_name,
            #         'lastname': user.last_name,
            #         'username': user.username,
            #         'rol': 'ADM'
            #     }   
            # Respuesta con confirmación de autenticación y tokens
            return Response({
                'confirmation': 'Autenticación exitosa',
                'user': user.username,
                'refresh': str(refresh),
                'access': str(refresh.access_token),
            })
        except Exception as e:
            return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# Vista para verificar tokens de acceso
class VerifyView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = TokenVerifySerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            access_token_obj = AccessToken(request.data['token'])
            user_id = access_token_obj['user_id']
            user = User.objects.get(id=user_id)

            # model_employee = None
            # if not user.username == 'system':
            #     model_employee = Employee.objects.select_related('user','job').get(document_number=user.username)
            #     if user.groups.first().id == 1: # Admin
            #         rol = 'ADM'
            #     elif user.groups.first().id == 2: # User
            #         rol = 'USU'
            #     elif user.groups.first().id == 3: # Supervisor
            #         rol = 'SUP'
            #     elif user.groups.first().id == 4: # Recursos Humanos
            #         rol = 'RHH'

            # if model_employee:
            #     user_info = {
            #         'id': model_employee.id if model_employee.id else "",
            #         'job_id': model_employee.job.id if model_employee.job.id else '',
            #         'job': model_employee.job.name if model_employee.job.name else '',
            #         'name': model_employee.complete_name(),
            #         'sede': model_employee.sede.name if model_employee.sede.name else '',
            #         'company': model_employee.company.business_name if model_employee.company.business_name else '',
            #         'username': user.username,
            #         'rol': rol if rol else ''
            #     }
            # else:
            #     user_info = {
            #         'name': user.first_name,
            #         'lastname': user.last_name,
            #         'username': user.username,
            #         'rol': 'ADM'
            #     }   
            # # Respuesta con información del usuario y token de acceso
            return Response({
                'user': user.username,
                'access': request.data['token'],
            })
        except TokenError as e:
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)


class EnvsView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):

        try:
            # Obtén todas las variables del objeto settings
            variables_settings = dir(settings)

            # Filtra las variables para excluir las que comienzan con '__' (atributos internos)
            variables_settings = [var for var in variables_settings if not var.startswith('__')]

            # Crea un diccionario con las variables y sus valores
            variables_dict = {var: getattr(settings, var) for var in variables_settings}

            # Respuesta con información del usuario y token de acceso
            return Response(variables_dict)
        except TokenError as e:
            return Response({'detail': str(e)}, status=status.HTTP_401_UNAUTHORIZED)

def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "Thank you for your email confirmation. Now you can login your account.")
        return redirect('https://inka-kappa.vercel.app')
    else:
        messages.error(request, "Activation link is invalid!")

    # return redirect('homepage')
        
class UserRegisterView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('first_name')
            second_name = request.data.get('second_name')
            last_name = request.data.get('last_name')
            second_last_name = request.data.get('second_last_name')
            document_number = request.data.get('document_number')

            if not email or not password or not document_number:
                return Response({'status': 'ERROR', 'msg': 'Faltan datos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

            if User.objects.filter(email=email).exists():
                return Response({'status': 'ERROR', 'msg': 'El correo electrónico ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=document_number, password=password, email=email, is_active=False)
            new_client = Client(
                user=user,
                first_name=first_name,
                second_name=second_name,
                last_name=last_name,
                second_last_name=second_last_name,
                document_number=document_number
            )
            new_client.save()

            activate_user(request, user, email)

            return Response({'status': 'OK', 'msg': 'Por favor, verifica tu correo electrónico y haz clic en el enlace de activación para completar tu registro. Nota: Revisa tu carpeta de spam.'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'ERROR', 'msg': 'Error al registrar el cliente.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

def activate_user(request, user, to_email):
    mail_subject = "Activa tu cuenta de usuario."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    
    email = EmailMessage(mail_subject, message, to=[to_email])
    email.content_subtype = "html"  # Esto asegura que el correo electrónico se envíe como HTML
    if email.send():
        messages.success(request, f'Estimado/a <b>{user}</b>, por favor ve a tu correo electrónico <b>{to_email}</b> y haz clic en el enlace de activación recibido para confirmar y completar el registro. <b>Nota:</b> Revisa tu carpeta de spam.')
    else:
        messages.error(request, f'Problema al enviar el correo electrónico a {to_email}, verifica si lo escribiste correctamente.')
