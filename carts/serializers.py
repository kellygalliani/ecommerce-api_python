from rest_framework import serializers
from .models import Cart, CartProducts
from products.serializers import ProductInCartSerializer
from products.models import Product


class CartSerializer(serializers.ModelSerializer):
    products = ProductInCartSerializer(many=True)

    class Meta:
        model = Cart
        fields = ['id', 'total_price', 'items', 'products']
        extra_kwargs = {
            'products': {'source':'products'}
        }
        read_only_fields = ['id']
        depth = 1

    def create(self, validated_data: dict, context) -> Cart:
        return Cart.objects.create(**validated_data)

    def update(self, instance, validated_data: dict, context):
        user = context['request'].user
        user_cart = Cart.objects.get(user=user)

        products_in_cart = {cp.product_id: cp for cp in user_cart.cartproducts_set.all()}

        products = validated_data.pop('products', [])

        total_price = 0

        for product_data in products:
            product_id = product_data['id']
            product_price = product_data['total_price']

            total_price += product_price

            quantity = product_data.get('quantity', 1)

            if product_id in products_in_cart:
                cart_product = products_in_cart[product_id]
                cart_product.quantity += quantity
                cart_product.save()
            else:
                product = Product.objects.get(pk=product_id)
                cart_product = CartProducts.object.create(cart=user_cart, product=product, quantity=quantity)

        for cart_product in products_in_cart.values():
            if cart_product.quantity == 0:
                    cart_product.delete()

        user_cart = Cart.objects.get(pk=user_cart.pk)
        cart_items = user_cart.cartproducts_set.all().count()
        
        instance.items = cart_items
        instance.total_price = total_price
        instance.save()

        return instance
