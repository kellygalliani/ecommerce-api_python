from rest_framework import generics, permissions
from .serializers import ProductSerializer
from .models import Product
from rest_framework_simplejwt.authentication import JWTAuthentication
from users.permissions import IsProductSellerOrAdmin
from rest_framework.permissions import AllowAny
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import PermissionDenied

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
        
        return serializer.save(seller=self.request.user)
    
class ProductDetailsView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsProductSellerOrAdmin]
    authentication_classes = [JWTAuthentication]



