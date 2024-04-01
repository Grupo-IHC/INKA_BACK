from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from api.models import *
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
import os
from urllib.parse import unquote
from datetime import datetime, timedelta
from django.db.models import Prefetch
from django.db.models import Q
from django.http import HttpResponse
import json
from django.db import transaction
from rest_framework.permissions import IsAuthenticated
from django.db.models import Count
from django.conf import settings
import boto3
from botocore.exceptions import ClientError
from django.core.exceptions import ObjectDoesNotExist
from django.core.files.storage import default_storage
from django.db.models import Q
import imghdr
from django.core.files.base import ContentFile 
from io import BytesIO
from django.http import HttpResponseBadRequest
import re
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

    return redirect('homepage')
        
class ClientGetPost(APIView):
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