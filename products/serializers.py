from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "stock",
            "price",
            "availability"
        ]

        def create(self, validated_data):
            return Product.objects.create(**validated_data)


class ProductInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "price",
            "availability",
        ]
        exclude = ["stock"]
