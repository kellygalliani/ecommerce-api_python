from rest_framework import permissions
from .models import OrderProducts
from products.models import Product
from rest_framework.exceptions import NotFound


class IsOrderSellerOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        if not request.user.is_authenticated:
            return False
        if request.user.is_superuser:
            return True
        order_id = view.kwargs['pk']
        try:
            order = OrderProducts.objects.filter(order_id=order_id).first()
            product = Product.objects.get(id=order.product_id)
        except OrderProducts.DoesNotExist:
            raise NotFound()
        return product.seller == request.user


class IsSeller(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_seller
