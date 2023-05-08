from rest_framework import permissions
from rest_framework.views import View
from .models import User


class IsAccountOwnerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view: View, obj: User) -> bool:
        return request.user.is_authenticated and (obj == request.user or request.user.is_superuser)


class IsProductSellerOrAdmin(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.seller == request.user or request.user.is_superuser
