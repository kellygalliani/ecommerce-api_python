from carts.models import Cart
from orders.models import Order, OrderProducts
from rest_framework import serializers
from rest_framework.exceptions import ValidationError
from products.models import Product
from products.serializers import ProductInCartSerializer
from users.models import User
from django.core.mail import send_mail
from django.conf import settings
from .exceptions import NoStockError


class OrderSerializer(serializers.ModelSerializer):
    product = ProductInCartSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ["id", "order_status", "total_price", "created_at", "product"]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True}
        }
        depth = 1

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        for product in representation['product']:
            product.pop('availability', None)
            product.pop('quantity', None)
        return representation

    def create(self, validated_data: dict) -> Order:
        cart = Cart.objects.get(id=validated_data["user"].cart.id)

        sellers = []

        if cart.items == 0:
            raise ValidationError({"message": 'Your cart is empty.'})

        for item in cart.cartproducts_set.all():
            product = Product.objects.get(id=item.product_id)

            if product.seller_id not in sellers:
                sellers.append(product.seller_id)

        for seller in sellers:
            products_list = []
            quantity = 0
            total_price = 0
            for item in cart.cartproducts_set.all():
                product = Product.objects.get(id=item.product_id)
                if product.seller_id == seller:
                    products_list.append(product)
                    quantity += item.quantity

                    if(product.stock == 0 or item.quantity > product.stock):
                        raise NoStockError({"message": "This product does not have enough items in stock."})

                    product.stock = product.stock - item.quantity
                    product.save()
                    total_price += product.price * item.quantity

            order_data = Order.objects.create(**validated_data)
            order_data.product.set(products_list)
            order_data.total_price = total_price
            order_data.save()

            order_products = OrderProducts.objects.filter(order_id=order_data.id)

            for order in order_products:
                order.quantity = quantity

                order.save()

        cart.products.clear()
        cart.total_price = 0
        cart.items = 0
        cart.save()

        send_mail(
            subject="Ecommerce Order",
            message=f"The order:{order_data.id} of total {order_data.total_price}, was completed successfully.",
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[validated_data["user"].email],
            fail_silently=False
        )

        return order_data

    def update(self, instance: Order, validated_data: dict) -> Order:

        for key, value in validated_data.items():
            if key == 'order_status':
                user = User.objects.get(id=instance.user_id)
                send_mail(
                    subject="Ecommerce Order",
                    message=f"The status of order {instance.id} has been updated to: {value}",
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[user.email],
                    fail_silently=False
                )
            setattr(instance, key, value)

        instance.save()

        return instance
