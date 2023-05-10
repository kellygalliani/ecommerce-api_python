from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from rest_framework.exceptions import NotAcceptable
from .models import User
from orders.models import Order, OrderProducts
from products.models import Product
from carts.models import Cart
from addresses.models import Address
from addresses.serializers import AddressSerializer


class UserSerializer(serializers.ModelSerializer):
    address = AddressSerializer()

    class Meta:
        model = User

        fields = [
            "id",
            "username",
            "email",
            "password",
            "first_name",
            "last_name",
            "is_superuser",
            "is_seller",
            "cart",
            "address",
        ]
        depth = 2
        read_only_fields = ["id", "cart"]
        extra_kwargs = {
            "username": {
                "validators": [
                    UniqueValidator(
                        queryset=User.objects.all(),
                        message="A user with that username already exists.",
                    )
                ],
            },
            "email": {
                "validators": [UniqueValidator(queryset=User.objects.all())],
            },
            "password": {"write_only": True},
        }

    def create(self, validated_data: dict) -> User:
        cart = Cart.objects.create()
        validated_data["cart"] = cart

        address_data = validated_data.pop("address", None)

        if address_data:
            address = Address.objects.create(**address_data)
            validated_data["address"] = address
        if validated_data.__contains__("is_superuser"):
            if validated_data["is_superuser"] == True:
                return User.objects.create_superuser(**validated_data)

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop("password", None)

        for key, value in validated_data.items():
            if key == "is_seller" and value == False:
                user = instance

                if user.is_seller:
                    products = Product.objects.filter(seller_id=user.id)
                    in_progress_order_found = False
                    if products:
                        for product in products:
                            orders = OrderProducts.objects.filter(
                                product_id=product.id
                            )
                            for order in orders:
                                in_started_order = (
                                    Order.objects.filter(id=order.order_id)
                                    .filter(order_status="PEDIDO REALIZADO")
                                    .first()
                                )
                                in_progress_order = (
                                    Order.objects.filter(id=order.order_id)
                                    .filter(order_status="PEDIDO REALIZADO")
                                    .first()
                                )
                                if in_started_order or in_progress_order:
                                    in_progress_order_found = True
                                else:
                                    product.stock = 0
                                    product.availability = False
                                    product.save()
                            if in_progress_order_found:
                                raise NotAcceptable(
                                    {
                                        "message": "This seller has in progress orders."
                                    }
                                )
                            if not in_progress_order_found:
                                user.is_seller = False
                                user.save()
            setattr(instance, key, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance
