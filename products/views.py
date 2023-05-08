from rest_framework import generics, permissions
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import AllowAny
from rest_framework.exceptions import PermissionDenied

from .serializers import ProductSerializer
from .models import Product

from users.permissions import IsProductSellerOrAdmin

from django.contrib.auth.models import AnonymousUser


class ProductReadAllView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsProductSellerOrAdmin]

    def get_permissions(self):
            if self.request.method in permissions.SAFE_METHODS:
                return [AllowAny()]
            return super().get_permissions()

    def perform_create(self, serializer):
        if self.request.user == AnonymousUser():
             raise PermissionDenied("Authentication credentials were not provided.")
        if not self.request.user.is_seller:
             raise PermissionDenied("Você não é cadastrado como um usuário vendedor.")
        
        return serializer.save(seller=self.request.user)
    
class ProductDetailsView(generics.RetrieveUpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsProductSellerOrAdmin]
    authentication_classes = [JWTAuthentication]

    def get_permissions(self):
            if self.request.method in permissions.SAFE_METHODS:
                return [AllowAny()]
            return super().get_permissions()


