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
            
            if type:
                model_product = model_product.filter(type_product=type)
                category_set = set() 
                category_data = []
                for product in model_product:
                    if product.category_product:
                        category_set.add(product.category_product.name)

                category_data = [{'name': category} for category in category_set]

            if category:
                model_product = model_product.filter(category_product=category)

            if not model_product.exists():
                return Response({'status': 'ERROR', 'msg': 'No hay productos registrados'}, status=status.HTTP_400_BAD_REQUEST)


            product_data = []
            type_data = []
            products_by_name = {}

            for product in model_product:

                if product.name in products_by_name:

                    products_by_name[product.name]['color'].add(str(product.color_product))
                else:

                    products_by_name[product.name] = {
                        # 'id': product.id,
                        'name': product.name,
                        # 'description': product.description,
                        # 'type_product': product.type_product.name,
                        'color': {str(product.color_product)},
                        # 'category_product': product.category_product.name if product.category_product else None,
                        # 'price': product.price,
                        # 'measure': product.measure,
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

class productGetByName(APIView):
    permission_classes = (AllowAny,)
    
    def get(self, request, product_name):
        try:
            model_products = Product.objects.filter(name=product_name).select_related('type_product', 'color_product', 'category_product')

            if not model_products.exists():
                return Response({'status': 'ERROR', 'msg': 'No hay productos registrados'}, status=status.HTTP_400_BAD_REQUEST)

            data = []

            products_by_name = {}

            for product in model_products:
                if product.name not in products_by_name:
                    products_by_name[product.name] = {
                        'id': {str(product.id)},
                        'name': product.name,
                        'description': product.description,
                        'type_product': product.type_product.name,
                        'color': {str(product.color_product)},
                        'category_product': product.category_product.name if product.category_product else None,
                        'price': product.price,
                        'measure': product.measure,
                        'image': product.image.url,
                    }
                else:
                    products_by_name[product.name]['id'].add(str(product.id))
                    products_by_name[product.name]['color'].add(str(product.color_product))

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
    
# class TypeGetById(APIView):
#     permission_classes = (AllowAny,)

#     def get(self, request, type_id):
#         try:
#             model_type_product = TypeProduct.objects.filter(id=type_id).first()
#             if not model_type_product:
#                 return Response({'status': 'ERROR', 'msg': 'El tipo de producto no existe'}, status=status.HTTP_400_BAD_REQUEST)
            
#             model_category_products = CategoryProduct.objects.filter(types=model_type_product.id)

#             data_categories = []
#             for category in model_category_products:
#                 data_categories.append({
#                     'id': category.id,
#                     'name': category.name,
#                     'description': category.description
#                 })
            
#             data = {
#                 'id': model_type_product.id,
#                 'name': model_type_product.name,
#                 'description': model_type_product.description,
#                 'category': data_categories
#             }
#             return Response({'status': 'OK', 'data': data}, status=status.HTTP_200_OK)
#         except Exception as e:
#             return Response({'status': 'ERROR', 'msg': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
