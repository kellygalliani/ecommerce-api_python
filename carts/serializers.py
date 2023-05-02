from rest_framework import serializers
from .models import Cart
from products.serializer import ProductInCartSerializer


class CartSerializer(serializers.ModelSerializer):
    products = ProductInCartSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'items', 'products']
        depth = 1

    def create(self, validated_data: dict) -> Cart:
        return Cart.objects.create(**validated_data)

    def update(self, instance: Cart, validated_data: dict) -> Cart:
        for key, value in validated_data.items():
            setattr(instance, key, value)

        instance.save()

        return instance