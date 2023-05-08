from rest_framework import permissions
from .models import Order, OrderProducts
from products.models import Product

class IsOrderSellerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        order_id = view.kwargs['pk']
        try:
            order = OrderProducts.objects.get(order_id=order_id)
            product = Product.objects.get(id=order.product_id)
        except Order.DoesNotExist:
            raise ValueError({'message': 'Order não existe.'})
        return product.seller == request.user


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_seller