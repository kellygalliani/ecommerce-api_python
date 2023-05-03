from rest_framework import generics
from .serializers import ProductSerializer
from .models import Product


class ProductReadAllView(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def perform_create(self, serializer):
        return serializer.save(seller_id=self.request.user.id)


class ProductDetailsView(generics.UpdateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
