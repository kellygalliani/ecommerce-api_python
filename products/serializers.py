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
            "availability",
            "seller_id"
        ]
        read_only_fields = ["id"]

        def create(self, validated_data):
            return Product.objects.create(**validated_data)

        def update(self, instance, validated_data):
            for key, value in validated_data.items():
                setattr(instance, key, value)

            if instance.stock <= 0:
                instance.availability = False
            else:
                instance.availability = True

            instance.save()

            return instance


class ProductInCartSerializer(serializers.ModelSerializer):

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "price",
            "seller_id",
            "availability"
        ]
        read_only_fields = ["id"]
