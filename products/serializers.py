from rest_framework import serializers
from .models import Product
from carts.models import CartProducts


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
    quantity = serializers.SerializerMethodField()

    def get_quantity(self, obj):
        cart = self.context.get('cart')
        if cart:
            cart_product = CartProducts.objects.filter(cart=cart, product=obj).first()
            if cart_product:
                return cart_product.quantity
        return None

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "category",
            "price",
            "seller_id",
            "availability",
            "quantity"
        ]
        read_only_fields = ["id"]
