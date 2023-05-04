from carts.models import CartProducts
from orders.models import Order
from rest_framework import serializers
import ipdb
from users.models import User

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
        # print("-" * 80, validated_data["user"])
        # print("-" * 80, validated_data)
        # print("-" * 80, validated_data["user"].cart.id)
        # print(validated_data.get("user").cart.products)
        cart_products = validated_data["user"].cart.products
        product_in_cart = CartProducts.objects.filter(
            cart_id=validated_data["user"].cart.id
        ).first()
        print("-" * 80, product_in_cart)

        for item in product_in_cart:
            print(item)

        order = Order.objects.create(**validated_data)
        # ipdb.set_trace()
        # order.user = user
        order.product.set(cart_products.all())
        return order

    def update(self, instance: Order, validated_data: dict) -> Order:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
