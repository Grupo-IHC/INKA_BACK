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
    permission_classes = (IsAuthenticated)

    def get(self, request):
        # Implementa la lógica para manejar solicitudes GET
        pass

    def post(self, request):
        order_details = request.data.getlist('order_detail') 

        client = request.data.get('client')
        price = request.data.get('price')
        address = request.data.get('address')
        contact = request.data.get('contact')
        contact_dni = request.data.get('contact_dni')
        quantity = request.data.get('quantity')
        type_delivery = request.data.get('type_delivery')
        method_payment = request.data.get('method_payment')

        id_orders = []

        for detail in order_details:
            product_instance = Product.objects.get(id=detail['product'])
            design_image = detail.get('design_image')
            order = Order.objects.create(
                product=product_instance,
                design=detail['design'],
                price=detail['price'],
                quantity=detail['quantity']
            )

            if design_image:
                order.design_image = design_image
                order.save()

            id_orders.append(order.id)

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



        