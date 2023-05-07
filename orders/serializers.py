from carts.models import CartProducts, Cart
from orders.models import Order, OrderProducts
from rest_framework import serializers
import ipdb
from users.models import User
from products.models import Product
from products.serializers import ProductInCartSerializer
from users.serializers import UserSerializer
from rest_framework.exceptions import ValidationError



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

    def create(self, validated_data: dict) -> Order:
        cart = Cart.objects.get(id=validated_data["user"].cart.id)

        sellers = []

        if cart.items == 0:
            raise ValidationError({"message": 'O carrinho está vazio.'})
        
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

        return order_data

    def update(self, instance: Order, validated_data: dict) -> Order:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance
