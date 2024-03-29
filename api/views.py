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

class ClientGetPost(APIView):
    def post(self, request):
        try:
            email = request.data.get('email')
            password = request.data.get('password')
            first_name = request.data.get('first_name')
            second_name = request.data.get('second_name')
            last_name = request.data.get('last_name')
            second_last_name = request.data.get('second_last_name')
            docucment_number = request.data.get('docucment_number')

            if not email:
                 return Response({'status': 'ERROR', 'msg': 'No se ha ingresado el email.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not password:
                return Response({'status': 'ERROR', 'msg': 'No se ha ingresado la contraseña.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if not docucment_number:
                return Response({'status': 'ERROR', 'msg': 'No se ha ingresado el numero de documento.'}, status=status.HTTP_400_BAD_REQUEST)

            new_client = Client(
                email=email,
                password=password,
                first_name=first_name,
                second_name=second_name,
                last_name=last_name,
                second_last_name=second_last_name,
                docucment_number=docucment_number
            )
            new_client.save()

            return Response({'status': 'OK', 'msg': 'Registro completado satifactoriamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'ERROR', 'msg': 'Error al obtener los datos.', 'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)