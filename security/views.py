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
from django.http import HttpResponse
import random
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
import datetime

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
            model_client = Client.objects.get(user=user)
            # Respuesta con confirmación de autenticación y tokens
            return Response({
                'confirmation': 'Autenticación exitosa',
                'user': user.username,
                'info_user': {
                    'first_name': model_client.first_name.upper(),
                    'last_name': model_client.last_name.upper(),
                    'email': model_client.email,
                    'document_number': model_client.document_number,
                },
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
            model_client = Client.objects.get(user=user)

            # # Respuesta con información del usuario y token de acceso
            return Response({
                'user': user.username,
                'info_user': {
                    'first_name': model_client.first_name.upper(),
                    'last_name': model_client.last_name.upper(),
                    'email': model_client.email,
                    'document_number': model_client.document_number,
                },
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
        return render(request, 'template_expired_code.html', {'status': 'ERROR', 'msg': 'Activation link is invalid!'})
        
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

            if not email.endswith('@gmail.com'):
                return Response({'status': 'ERROR', 'msg': 'Por favor, utiliza una dirección de correo electrónico de Gmail.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if User.objects.filter(email=email).exists():
                return Response({'status': 'ERROR', 'msg': 'El correo electrónico ya está registrado.'}, status=status.HTTP_400_BAD_REQUEST)

            user = User.objects.create_user(username=document_number, password=password, email=email, is_active=False)
            new_client = Client(
                user=user,
                first_name=first_name,
                second_name=second_name,
                last_name=last_name,
                second_last_name=second_last_name,
                document_number=document_number,
                email=email
            )
            new_client.save()

            activate_user(request, user, email)

            return Response({'status': 'OK', 'msg': 'Por favor, verifica tu correo electrónico y haz clic en el enlace de activación para completar tu registro. Revisa tu carpeta de spam.'}, status=status.HTTP_200_OK)
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

class ContactView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            name = request.data.get('name')
            email = request.data.get('email')
            mail_subject = request.data.get('mail_subject')
            message = request.data.get('message')

            if not name or not email or not mail_subject or not message:
                return Response({'status': 'ERROR', 'msg': 'Faltan datos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

            if not email.endswith('@gmail.com'):
                return Response({'status': 'ERROR', 'msg': 'Por favor, utiliza una dirección de correo electrónico de Gmail.'}, status=status.HTTP_400_BAD_REQUEST)
            
            message = render_to_string("template_contact.html", {
                'name': name,
                'email': email,
                'mail_subject': mail_subject,
                'message': message
            })
            
            email = EmailMessage(mail_subject, message, to=[settings.EMAIL_HOST_USER])
            email.content_subtype = "html" 
            if email.send():
                return Response({'status': 'OK', 'msg': 'Mensaje enviado correctamente.'}, status=status.HTTP_200_OK)
            else:
                return Response({'status': 'ERROR', 'msg': 'Problema al enviar el mensaje.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'status': 'ERROR', 'msg': 'Error al enviar el mensaje.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

import string

class ResetPasswordView(APIView):
    permission_classes = (AllowAny,)

    CODIGO_VALIDEZ_MINUTOS = 15
    
    def generar_codigo_verificacion(self):
        caracteres = string.ascii_uppercase + string.digits
        print(caracteres)
        return ''.join(random.choices(caracteres, k=4))

    def guardar_codigo_verificacion_en_sesion(self, request, codigo):
        fecha_generacion = datetime.datetime.now()
        request.session['codigo_verificacion_generado'] = fecha_generacion.isoformat()
        request.session['codigo_verificacion'] = codigo
        print("......... guardar codigo verificacion en sesion .........")
        print(f'Codigo de verificacion: {codigo}')
        print(f'Fecha de generacion: {fecha_generacion}')
        print("......... fin .........")

    def eliminar_codigo_verificacion_de_sesion(self, request):
        if 'codigo_verificacion' in request.session:
            del request.session['codigo_verificacion']

    def verificar_codigo_verificacion(self, request, codigo):
        print("......... verificar_code .........")
        if 'codigo_verificacion' not in request.session or 'codigo_verificacion_generado' not in request.session:
            print("entre al erro de verificar no hay codigo en sesion")
            return False
        
        print(f'Codigo ingresado: {codigo}')
        print(f'Codigo guardado en la sesion: {request.session["codigo_verificacion"]}')
        
        fecha_generacion_str = request.session['codigo_verificacion_generado']
        fecha_generacion = datetime.datetime.fromisoformat(fecha_generacion_str)
        fecha_actual = datetime.datetime.now()
        tiempo_transcurrido = fecha_actual - fecha_generacion

        if tiempo_transcurrido.total_seconds() > (self.CODIGO_VALIDEZ_MINUTOS * 60):
            self.eliminar_codigo_verificacion_de_sesion(request)
            print("......... vencio el token por tiempo .........")
            return False

        codigo_guardado = request.session['codigo_verificacion']
        if codigo_guardado and codigo == codigo_guardado:
            print("......... validando .........")
            print(codigo_guardado)
            print(codigo) 
            print("......... valide que son iguales .........")
            return True
        else:
            print("......... no son iguales .........")
            return False
    
    def post(self, request):
        try:
            email = request.data.get('email')
            codigo_ingresado = request.data.get('code')
            print(f'Codigo ingresado: {codigo_ingresado}')
            print(f'Email ingresado: {email}')
            if not email:
                return Response({'status': 'ERROR', 'msg': 'Faltan datos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

            if not email.endswith('@gmail.com'):
                return Response({'status': 'ERROR', 'msg': 'Por favor, utiliza una dirección de correo electrónico de Gmail.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not User.objects.filter(email=email, is_active=True).exists():
                return Response({'status': 'ERROR', 'msg': 'El correo electrónico no está registrado.'}, status=status.HTTP_400_BAD_REQUEST)
            
            user = User.objects.get(email=email)
            client = Client.objects.get(user=user)
            
            if not codigo_ingresado:
                codigo_verificacion = self.generar_codigo_verificacion()
                self.guardar_codigo_verificacion_en_sesion(request, codigo_verificacion)
                
                mail_subject = "Restablecer contraseña."
                message = render_to_string("template_reset_password.html", {
                    'user': client.first_name.upper() + ' ' + client.last_name.upper(),
                    'random_number': codigo_verificacion
                })

                email = EmailMessage(mail_subject, message, to=[email])
                email.content_subtype = "html" 
                if email.send():
                    return Response({'status': 'OK', 'msg': 'Por favor, verifica tu correo electrónico y haz clic en el enlace de restablecimiento de contraseña. Revisa tu carpeta de spam.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'ERROR', 'msg': 'Problema al enviar el correo electrónico.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            else:
                if self.verificar_codigo_verificacion(request, codigo_ingresado):
                    return Response({'status': 'OK', 'msg': 'Código de verificación válido. Puedes cambiar tu contraseña.'}, status=status.HTTP_200_OK)
                else:
                    return Response({'status': 'ERROR', 'msg': 'Código de verificación incorrecto.'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'status': 'ERROR', 'msg': 'Error al procesar la solicitud.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
from django.core.exceptions import ObjectDoesNotExist

class ChangePasswordView(APIView):
    permission_classes = (AllowAny,)

    def post(self, request):
        try:
            email = request.data.get('email')
            codigo_verificacion = request.data.get('code')
            nueva_contrasena = request.data.get('new_password')

            if not email or not codigo_verificacion or not nueva_contrasena:
                return Response({'status': 'ERROR', 'msg': 'Faltan datos requeridos.'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                user = User.objects.get(email=email)
            except ObjectDoesNotExist:
                return Response({'status': 'ERROR', 'msg': 'No se encontró un usuario con ese correo electrónico.'}, status=status.HTTP_400_BAD_REQUEST)

            reset_view = ResetPasswordView()
            if not reset_view.verificar_codigo_verificacion(request, codigo_verificacion):
                return Response({'status': 'ERROR', 'msg': 'Código de verificación incorrecto o expirado.'}, status=status.HTTP_400_BAD_REQUEST)

            user.set_password(nueva_contrasena)
            user.save()

            reset_view.eliminar_codigo_verificacion_de_sesion(request)

            return Response({'status': 'OK', 'msg': 'Contraseña cambiada exitosamente.'}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'ERROR', 'msg': 'Error al cambiar la contraseña.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


