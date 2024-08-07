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
from collections import defaultdict
# Create your views here.

class productGetPost(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            type = request.query_params.get('type')
            category = request.query_params.get('category')
            model_product = Product.objects.all().select_related('type_product', 'color_product', 'category_product')
            
            product_data = []
            type_data = []
            products_by_name = {}

            if type:
                model_product = model_product.filter(type_product=type)
                category_set = set() 
                category_data = []
                for product in model_product:
                    if product.category_product:
                        category_set.add((product.category_product.id, product.category_product.name))

                category_data = [{'id': category[0], 'name': category[1]} for category in category_set]

            if category:
                model_product = model_product.filter(category_product=category)

            if not model_product.exists():
                return Response({'status': 'ERROR', 'msg': 'No hay productos registrados' , 'type': type_data,'product': product_data, 'category': category_data}, status=status.HTTP_400_BAD_REQUEST)

            for product in model_product:

                if product.name in products_by_name:

                    products_by_name[product.name]['color'].add(str(product.color_product))
                else:

                    products_by_name[product.name] = {
                        'name': product.name,
                        'code': product.code,
                        'color': {str(product.color_product)},
                        'image': product.image.url,
                    }

                    type_data = {
                        'name': product.type_product.name,
                        'description': product.type_product.description,
                    }


            product_data = list(products_by_name.values())

            return Response({'status': 'OK', 'type': type_data,'product': product_data, 'category': category_data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'ERROR', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request):
        try:
            required_fields = ['name', 'description',  'type_product', 'color_product', 'category_product', 'price', 'measure', 'image']
            for field in required_fields:
                if not request.data.get(field):
                    return Response({'status': 'ERROR', 'msg': f'El campo {field} es obligatorio'}, status=status.HTTP_400_BAD_REQUEST)

            model_type_product = TypeProduct.objects.filter(id=request.data.get('type_product')).first()
            model_color_product = ColorProduct.objects.filter(id=request.data.get('color_product')).first()
            model_category_product = CategoryProduct.objects.filter(id=request.data.get('category_product')).first()

            if not all([model_type_product, model_color_product]):
                return Response({'status': 'ERROR', 'msg': 'Uno o más elementos relacionados no existen'}, status=status.HTTP_400_BAD_REQUEST)

            model_product = Product.objects.create(
                name=request.data.get('name'),
                description=request.data.get('description'),
                type_product=model_type_product,
                color_product=model_color_product,
                category_product=model_category_product,
                price=request.data.get('price'),
                measure=request.data.get('measure'),
                image=request.data.get('image')
            )
            return Response({'status': 'OK', 'msg': 'Producto registrado correctamente'}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'status': 'ERROR', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class productGetByCode(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, code):
        try:
            model_products = Product.objects.filter(code=code).select_related('type_product', 'color_product', 'category_product')

            if not model_products.exists():
                return Response({'status': 'ERROR', 'msg': 'No hay productos registrados'}, status=status.HTTP_400_BAD_REQUEST)

            data = []

            products_by_name = {}

            for product in model_products:
                if product.code not in products_by_name:
                    products_by_name[product.code] = {
                        'id': {str(product.id)},
                        'name': product.name,
                        'description': product.description if product.description else None,
                        'type_product': product.type_product.name,
                        'color': {str(product.color_product)},
                        'category_product': product.category_product.name if product.category_product else None,
                        'price': product.price,
                        'measure': product.measure,
                        'image': product.image.url,
                        'stock': [str(product.stock)]
                    }
                else:
                    products_by_name[product.code]['id'].add(str(product.id))
                    products_by_name[product.code]['color'].add(str(product.color_product))
                    products_by_name[product.code]['stock'].append(str(product.stock))

            data = list(products_by_name.values())

            return Response({'status': 'OK', 'data': data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'ERROR', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
        
class productFilterName(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        try:
            name = request.query_params.get('name')
            if not name:
                return Response({'status': 'ERROR', 'msg': 'El campo de busqueda está vacío. Por favor, agregue un código o palabra que identifique el producto que busca.'}, status=status.HTTP_400_BAD_REQUEST)
            
            if len(name) < 2:
                return Response({'status': 'ERROR', 'msg': 'Para relizar la busqueda la palabra debe contener minimo 2 caracteres.'}, status=status.HTTP_400_BAD_REQUEST)
            keywords = name.split()

            query = Q()
            for keyword in keywords:
                query |= Q(name__icontains=keyword)
            
            model_products = Product.objects.filter(query).select_related('type_product', 'color_product', 'category_product')

            if not model_products.exists():
                return Response({'status': 'ERROR', 'msg': 'No hay productos registrados'}, status=status.HTTP_400_BAD_REQUEST)

            data = []

            products_by_name = {}

            for product in model_products:

                if product.name in products_by_name:

                    products_by_name[product.name]['color'].add(str(product.color_product))
                else:

                    products_by_name[product.name] = {
                        'name': product.name,
                        'code': product.code,
                        'price': product.price,
                        'color': {str(product.color_product)},
                        'image': product.image.url,
                    }

                    type_data = {
                        'name': product.type_product.name,
                        'description': product.type_product.description,
                    }


            data = list(products_by_name.values())

            return Response({'status': 'OK', 'data': data}, status=status.HTTP_200_OK)

        except Exception as e:
            return Response({'status': 'ERROR', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


        
