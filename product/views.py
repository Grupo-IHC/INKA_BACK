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

# Create your views here.

class productGetPost(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            category = request.query_params.get('category')

            model_product = Product.objects.all().select_related('category_product','type_product','color_product')
            
            if category:
                model_product = model_product.filter(category_product=category)

            if not model_product.exists():
                return Response({'status': 'ERROR','msg': 'No hay productos registrados'}, status=status.HTTP_400_BAD_REQUEST)
            
            if model_product.exists():
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
                return Response({'status': 'OK','data': data}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'ERROR','msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            name = request.data.get('name')
            description = request.data.get('description')
            category_product = request.data.get('category_product')
            type_product = request.data.get('type_product')
            color_product = request.data.get('color_product')
            price = request.data.get('price')
            measure = request.data.get('measure')
            image = request.data.get('image')

            if not name:
                return Response({'status': 'ERROR','msg': 'El campo nombre es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
            if not description:
                return Response({'status': 'ERROR','msg': 'El campo descripción es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
            if not category_product:
                return Response({'status': 'ERROR','msg': 'El campo categoría de producto es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
            if not type_product:
                return Response({'status': 'ERROR','msg': 'El campo tipo de producto es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
            if not color_product:
                return Response({'status': 'ERROR','msg': 'El campo color de producto es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
            if not price:
                return Response({'status': 'ERROR','msg': 'El campo precio es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
            if not measure:
                return Response({'status': 'ERROR','msg': 'El campo medida es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
            if not image:
                return Response({'status': 'ERROR','msg': 'El campo imagen es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

            model_category_product = CategoryProduct.objects.filter(id=category_product).first()
            if not model_category_product:
                return Response({'status': 'ERROR','msg': 'La categoría de producto no existe'}, status=status.HTTP_400_BAD_REQUEST)

            model_type_product = TypeProduct.objects.filter(id=type_product).first()
            if not model_type_product:
                return Response({'status': 'ERROR','msg': 'El tipo de producto no existe'}, status=status.HTTP_400_BAD_REQUEST)

            model_color_product = ColorProduct.objects.filter(id=color_product).first()
            if not model_color_product:
                return Response({'status': 'ERROR','msg': 'El color de producto no existe'}, status=status.HTTP_400_BAD_REQUEST)

            model_product = Product.objects.create(
                name = name,
                description = description,
                category_product = model_category_product,
                type_product = model_type_product,
                color_product = model_color_product,
                price = price,
                measure = measure,
                image = image
            )
            return Response({'status': 'OK','msg': 'Producto registrado correctamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'ERROR','msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class productGetById(APIView):
    permission_classes = (IsAuthenticated,)
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
    permission_classes = (IsAuthenticated,)
    def get(self, request):
        try:
            model_type_product = TypeProduct.objects.all()
            if not model_type_product.exists():
                return Response({'status': 'ERROR','msg': 'No hay tipos de producto registrados'}, status=status.HTTP_400_BAD_REQUEST)
            
            if model_type_product.exists():
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

    def post(self, request):
        try:
            name = request.data.get('name')
            if not name:
                return Response({'status': 'ERROR','msg': 'El campo nombre es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)
            
            model_type_product = TypeProduct.objects.create(
                name = name
            )
            return Response({'status': 'OK','msg': 'Tipo de producto registrado correctamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'ERROR','msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
