from django.shortcuts import render
from rest_framework.views import APIView
from sales.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
import boto3
from botocore.exceptions import ClientError
from rest_framework.permissions import AllowAny

# Create your views here.

class SaleGetPost(APIView):
    # parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            order_details = request.data.get('order_detail')
            price = request.data.get('price_total')
            address = request.data.get('address')
            contact = request.data.get('contact')
            contact_dni = request.data.get('contact_dni')
            quantity = request.data.get('quantity')
            type_delivery = request.data.get('type_delivery')
            method_payment = request.data.get('method_payment')

            id_orders = []
            insufficient_stock_products = []

            for detail in order_details:
                product_id = detail.get('product')
                product_instance = Product.objects.get(id=product_id)
                design_image = detail.get('design_image')
                price = detail.get('price')
                order_quantity = detail.get('quantity')

                # Verificar si hay suficiente stock
                if product_instance.stock < order_quantity:
                    insufficient_stock_products.append(product_instance.name)
                else:
                    # Restar el stock disponible
                    product_instance.stock -= order_quantity
                    product_instance.save()

                    order = Order.objects.create(
                        product=product_instance,
                        desing=design_image,
                        price=price,
                        quantity=order_quantity
                    )

                    id_orders.append(order.id)

            if insufficient_stock_products:
                message = f"No hay suficiente stock para los siguientes productos: {', '.join(insufficient_stock_products)}"
                return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        

            user = request.user.username
            instance_client = Client.objects.get(document_number=user)
            instance_type_delivery = TypeDelivery.objects.get(id=type_delivery)
            instance_method_payment = MethodPayment.objects.get(id=method_payment)

            order_detail_obj = Pedido.objects.create(
                client=instance_client,
                price=price,
                address=address,
                contact=contact,
                contact_dni=contact_dni,
                quantity=quantity,
                type_delivery=instance_type_delivery,
                method_payment=instance_method_payment
            )
            order_detail_obj.order.set(id_orders)

            return Response({"message": "Venta creada correctamente"}, status=status.HTTP_201_CREATED)
    
        except Exception as e:
                return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class shoppingGet(APIView):
    permission_classes = (IsAuthenticated,)

    def get(self, request):
        user = request.user.username
        instance_client = Client.objects.get(document_number=user)
        model_pedido = Pedido.objects.filter(client=instance_client)
        data = []
        for order_detail in model_pedido:
            order_items = []
            for item in order_detail.order.all():
                order_items.append({
                    "product_id": item.product.id,
                    "product_name": item.product.name,
                    "quantity": item.quantity,
                    "design": item.desing if item.desing else "No se proporcionó diseño",
                    "price": item.price
                })
            order_data = {
                "id": order_detail.id,
                "price": order_detail.price,
                "address": order_detail.address if order_detail.address else "El producto se entregará en tienda",
                "contact": order_detail.contact,
                "contact_dni": order_detail.contact_dni,
                "quantity": order_detail.quantity,
                "type_delivery": order_detail.type_delivery.name,
                "method_payment": order_detail.method_payment.name,
                "order": order_items
            }
            data.append(order_data)
        return Response(data, status=status.HTTP_200_OK)

class DesignGetPost(APIView):
    permission_classes = (AllowAny,)
    def post(self, request):
        try:
            # Verificar si se proporcionaron imágenes
            if 'desing' not in request.FILES:
                return Response({'error': 'No se proporcionaron imágenes.'}, status=status.HTTP_400_BAD_REQUEST)

            # Obtener la lista de imágenes del request
            design_files = request.FILES.getlist('desing')

            # Configurar el cliente de AWS S3
            s3 = boto3.client('s3')

            uploaded_image_urls = []

            # Iterar sobre cada imagen y subirla a AWS S3
            for design_file in design_files:
                # Generar una clave única para la imagen en el bucket de S3
                s3_key = f"desing/{design_file.name}"

                # Subir la imagen al bucket de S3
                s3.upload_fileobj(design_file, 'aws-sellos', s3_key, ExtraArgs={'ContentType': "image/png"})

                # Obtener la URL pública de la imagen cargada
                image_url = f"https://aws-sellos.s3.amazonaws.com/{s3_key}"
                
                # Agregar la URL de la imagen a la lista de URLs cargadas
                uploaded_image_urls.append({'nombre_archivo': design_file.name, 'url': image_url})

            return Response({'status': 'OK', 'imagenes_subidas': uploaded_image_urls}, status=status.HTTP_201_CREATED)
        except Exception as e:
            return Response({'error': f'Error al cargar las imágenes: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    def delete(self, request):
        try:
            # Obtener la clave del archivo a eliminar del request
            name = request.data.get('name')
            
            s3_key = f"desing/{name}"

            # Configurar el cliente de AWS S3
            s3 = boto3.client('s3')

            # Eliminar el archivo del bucket de S3
            s3.delete_object(Bucket='aws-sellos', Key=s3_key)

            return Response({'status': 'OK', 'msg': 'Imagen eliminada exitosamente.'}, status=status.HTTP_200_OK)
        except ClientError as e:
            if e.response['Error']['Code'] == 'NoSuchKey':
                return Response({'error': 'La imagen no existe en el bucket de AWS S3.'}, status=status.HTTP_404_NOT_FOUND)
            else:
                return Response({'error': f'Error al eliminar la imagen: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({'error': f'Error al eliminar la imagen: {e}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)





        