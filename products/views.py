from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .serializers import ProductSerializer
from .models import Product


class ProductReadAllView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        return serializer.save(seller=self.request.user)


class ProductDetailsView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
