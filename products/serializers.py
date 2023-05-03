from rest_framework import serializers
from .models import Product


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "stock",
            "price",
            "availability"
            "seller_id"
        ]
        read_only_fields = ["id"]

        def create(self, validated_data):
            return Product.objects.create(**validated_data)

        def update(self, instance, validated_data):
            for key, value in validated_data.items():
                setattr(instance, key, value)
            
            instance.save()

            return instance


class ProductInCartSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = [
            "name",
            "category",
            "price",
            "seller_id",
            "availability",
        ]
        read_only_fields = ["id"]
        exclude = ["stock"]
