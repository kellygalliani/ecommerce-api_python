from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated

from django.shortcuts import get_object_or_404

from .models import Cart
from .serializers import CartSerializer


class CartView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_field = 'product_id'
    serializer_class = CartSerializer

    def get_object(self):
        return Cart.objects.get(user=self.request.user)
    
    def perform_update(self, serializer):
        products = self.kwargs.get('product_id')
        quantity = self.request.data
        serializer.save(user=self.request.user, products=products, context=quantity)
