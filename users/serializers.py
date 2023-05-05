from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import User
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
        read_only_fields = ["id", "is_superuser", "cart"]
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

        return User.objects.create_user(**validated_data)

    def update(self, instance: User, validated_data: dict) -> User:
        password = validated_data.pop("password", None)

        for key, value in validated_data.items():
            setattr(instance, key, value)

        if password:
            instance.set_password(password)

        instance.save()

        return instance
