from rest_framework import serializers

from django.forms.models import model_to_dict

from .models import Cart, CartProducts

from products.serializers import ProductInCartSerializer
from products.models import Product


class CartSerializer(serializers.ModelSerializer):
    products = ProductInCartSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'items', 'products']
        read_only_fields = ['id']
        depth = 1

    def create(self, validated_data: dict) -> Cart:
        return Cart.objects.create(**validated_data)

    def update(self, instance, validated_data):
        product = Product.objects.get(id=int(validated_data['products']))

        quantity = validated_data['context']['quantity']

        found_product = CartProducts.objects.filter(cart_id=instance.id).filter(product_id=product).first()

        if found_product:
            found_product.quantity += quantity
            found_product.save()
        else:
            instance.products.add(product)
            product_in_cart = CartProducts.objects.filter(cart_id=instance.id).filter(product_id=product).first()
            product_in_cart.quantity = quantity
            product_in_cart.save()

        cart = CartProducts.objects.filter(cart_id=instance.id)
        
        price = 0
        items = 0
        for item in instance.cartproducts_set.all():
            price += item.quantity * item.product.price
            items += item.quantity

        instance.total_price = price
        instance.items = items
        instance.save()

        return instance
