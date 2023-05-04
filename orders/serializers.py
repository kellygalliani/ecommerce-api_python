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
        # print("-" * 80, validated_data["user"])
        # print("-" * 80, validated_data)
        # print("-" * 80, validated_data["user"].cart.id)
        # print(validated_data.get("user").cart.products)
        cart_products = validated_data["user"].cart.products
        cart = Cart.objects.get(id=validated_data["user"].cart.id)

        product_in_cart = CartProducts.objects.filter(
            cart_id=validated_data["user"].cart.id
        ).first()
        print("-" * 80, product_in_cart)

        sellers = []
        for item in cart.cartproducts_set.all():
            # print(item.product_id)
            product = Product.objects.get(id=item.product_id)
            # print(product.seller_id)
            if product.seller_id not in sellers:
                sellers.append(product.seller_id)
        orders = []
        for seller in sellers:
            products_list = []
            for item in cart.cartproducts_set.all():
                product = Product.objects.get(id=item.product_id)
                if product.seller_id == seller:
                    products_list.append(product)
            # ipdb.set_trace()
            # print(products_list)
            order = Order.objects.create(**validated_data)
            order.product.set(products_list)
            # order_id = order.id
            # order_made = Order.objects.get(id=order_id)
            # orders.append(order_made)

            # print(order.id)
        # for order in orders:
        # order_product = OrderProducts.objects.get(order_id=order.id)

        # ipdb.set_trace()
        # order.user = user

        # order.product.set(cart_products.all())
        # return OrderProducts.objects.get(id=)
        return self

    def update(self, instance: Order, validated_data: dict) -> Order:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
