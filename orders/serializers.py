from carts.models import CartProducts, Cart
from orders.models import Order, OrderProducts
from rest_framework import serializers
import ipdb
from users.models import User
from products.models import Product
from users.serializers import UserSerializer


class OrderSerializer(serializers.ModelSerializer):
    user = UserSerializer(read_only=True)

    class Meta:
        model = Order
        fields = ["id", "order_status", "total_price", "created_at", "user"]
        extra_kwargs = {
            "id": {"read_only": True},
            "created_at": {"read_only": True},
        }
        depth = 2

    def create(self, validated_data: dict) -> Order:
        cart = Cart.objects.get(id=validated_data["user"].cart.id)

        sellers = []
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
                    total_price += product.price * item.quantity

            order = Order.objects.create(**validated_data)
            order.product.set(products_list)
            order.total_price = total_price
            order.save()

            order_products = OrderProducts.objects.filter(order_id=order.id)

            for order in order_products:
                order.quantity = quantity

                order.save()

        return order

    def update(self, instance: Order, validated_data: dict) -> Order:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
