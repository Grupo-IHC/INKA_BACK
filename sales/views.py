from django.shortcuts import render
from rest_framework.views import APIView
from sales.models import *
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated

# Create your views here.

class SaleGetPost(APIView):
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = (IsAuthenticated,)

    def post(self, request):
        try:
            order_details = request.data.getlist('order_detail')
            price = request.data.get('price')
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
                        design=detail['design'],
                        price=detail['price'],
                        quantity=order_quantity
                    )

                    if design_image:
                        order.design_image = design_image
                        order.save()

                    id_orders.append(order.id)

            if insufficient_stock_products:
                message = f"No hay suficiente stock para los siguientes productos: {', '.join(insufficient_stock_products)}"
                return Response({"message": message}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({"message": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        user = request.user.username
        instance_client = Client.objects.get(document_number=user)
        instance_type_delivery = TypeDelivery.objects.get(id=type_delivery)
        instance_method_payment = MethodPayment.objects.get(id=method_payment)

        order_detail_obj = OrderDetail.objects.create(
            order=id_orders,
            client=instance_client,
            price=price,
            address=address,
            contact=contact,
            contact_dni=contact_dni,
            quantity=quantity,
            type_delivery=instance_type_delivery,
            method_payment=instance_method_payment
        )

        return Response({"message": "Venta creada correctamente"}, status=status.HTTP_201_CREATED)
    
class shoppingGet(APIView):
    permission_classes = (IsAuthenticated)

    def get(self, request):
        user = request.user.username
        instance_client = Client.objects.get(document_number=user)
        order = Order.objects.filter(client=instance_client)
        data = []
        for order_detail in order:
            order_data = {
                "id": order_detail.id,
                "order": order_detail.order,
                "price": order.price,
                "address": order.address,
                "contact": order.contact,
                "contact_dni": order.contact_dni,
                "quantity": order.quantity,
                "type_delivery": order.type_delivery.name,
                "method_payment": order.method_payment.name
            }
            data.append(order_data)
        return Response(data, status=status.HTTP_200_OK)





        