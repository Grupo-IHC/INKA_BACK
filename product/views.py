from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework import status
from product.models import *
from rest_framework.response import Response
from datetime import datetime, timedelta
from django.db.models import Prefetch
from django.db.models import Q
from django.http import HttpResponse
import json
from urllib.parse import unquote
import requests
import os
from itertools import chain
from django.db.models import Prefetch
from rest_framework.permissions import AllowAny
from rest_framework import generics
from django.db import transaction
from django.conf import settings
import boto3
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from django.core.files.storage import default_storage
from django.db.models import Count
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import ValidationError

# Create your views here.

class productGetPost(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            category = request.query_params.get('category')
            model_product = Product.objects.all().select_related('category_product', 'type_product', 'color_product')

            if category:
                model_product = model_product.filter(category_product=category)

            if not model_product.exists():
                return Response({'status': 'ERROR', 'msg': 'No hay productos registrados'}, status=status.HTTP_400_BAD_REQUEST)

            data = []
            for product in model_product:
                data.append({
                    'id': product.id,
                    'name': product.name,
                    'description': product.description,
                    'category_product': product.category_product.name,
                    'type_product': product.type_product.name,
                    'color_product': product.color_product.name,
                    'price': product.price,
                    'measure': product.measure,
                    'image': product.image.url,
                })
            return Response({'status': 'OK', 'data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'ERROR', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            required_fields = ['name', 'description', 'category_product', 'type_product', 'color_product', 'price', 'measure', 'image']
            for field in required_fields:
                if not request.data.get(field):
                    return Response({'status': 'ERROR', 'msg': f'El campo {field} es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

            model_category_product = CategoryProduct.objects.filter(id=request.data.get('category_product')).first()
            model_type_product = TypeProduct.objects.filter(id=request.data.get('type_product')).first()
            model_color_product = ColorProduct.objects.filter(id=request.data.get('color_product')).first()

            if not all([model_category_product, model_type_product, model_color_product]):
                return Response({'status': 'ERROR', 'msg': 'Uno o más elementos relacionados no existen'}, status=status.HTTP_400_BAD_REQUEST)

            model_product = Product.objects.create(
                name=request.data.get('name'),
                description=request.data.get('description'),
                category_product=model_category_product,
                type_product=model_type_product,
                color_product=model_color_product,
                price=request.data.get('price'),
                measure=request.data.get('measure'),
                image=request.data.get('image')
            )
            return Response({'status': 'OK', 'msg': 'Producto registrado correctamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'ERROR', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        
class productGetById(APIView):
    permission_classes = (AllowAny,)
    def get(self, request, product_id):
        try:
            model_product = Product.objects.filter(id=product_id).select_related('category_product','type_product','color_product').first()
            if not model_product:
                return Response({'status': 'ERROR','msg': 'El producto no existe'}, status=status.HTTP_400_BAD_REQUEST)
            
            data = {
                'id': model_product.id,
                'name': model_product.name,
                'description': model_product.description,
                'category_product': model_product.category_product.name,
                'type_product': model_product.type_product.name,
                'color_product': model_product.color_product.name,
                'price': model_product.price,
                'measure': model_product.measure,
                'image': model_product.image.url,
            }
            return Response({'status': 'OK','data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'ERROR','msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class typeGetPost(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            model_type_product = TypeProduct.objects.all()
            if not model_type_product.exists():
                return Response({'status': 'ERROR','msg': 'No hay tipos de producto registrados'}, status=status.HTTP_400_BAD_REQUEST)
            
            data = []
            for type_product in model_type_product:
                data.append({
                    'id': type_product.id,
                    'name': type_product.name,
                    'description': type_product.description,
                })
            return Response({'status': 'OK','data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'ERROR','msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @transaction.atomic
    def post(self, request):
        try:
            name = request.data.get('name')
            if not name:
                return Response({'status': 'ERROR','msg': 'El campo nombre es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
            
            model_type_product = TypeProduct.objects.create(
                name=name
            )
            return Response({'status': 'OK','msg': 'Tipo de producto registrado correctamente'}, status=status.HTTP_200_OK)
        except ValidationError as e:
            return Response({'status': 'ERROR','msg': str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'status': 'ERROR','msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class typeGetById(APIView):
    permission_classes = (AllowAny,)

    def get(self, request, type_id):
        try:
            model_type_product = TypeProduct.objects.filter(id=type_id).first()
            if not model_type_product:
                return Response({'status': 'ERROR','msg': 'El tipo de producto no existe'}, status=status.HTTP_400_BAD_REQUEST)
            
            model_category_product = CategoryProduct.objects.all()

            
            for category in model_category_product:
                if model_type_product.id == 'ff3c7b6c-83db-41c2-9d37-ceb325bc879d' or model_type_product.id == '1716490f-b25b-4ca3-ba9c-957c545e285a':
                    data_category = {
                        'name': 'TODOS'
                    }
                
                if model_type_product.id == '11c4d953-d310-4eb0-9438-1bb15769f146':
                    data_category = {
                        'id': category.id,
                        'name': category.name
                    }
                
                if model_type_product.id == '9cede5ca-b93d-4989-a60c-2403c32504eb':
                    data_category = {
                        'id': category.id,
                        'name': category.name
                    }
            data = {
                'id': model_type_product.id,
                'name': model_type_product.name,
                'description': model_type_product.description,
                'category_product': data_category
            }
            return Response({'status': 'OK','data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'ERROR','msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
