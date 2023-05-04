from django.shortcuts import render
from rest_framework import generics
from carts.models import Cart
from orders.models import Order

# Create your views here.
from orders.serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from users.models import User
import ipdb
from rest_framework_simplejwt.authentication import JWTAuthentication


class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    # queryset = Order.objects.all()
    serializer_class = OrderSerializer
    

    # def get_queryset(self):
    #     return Cart.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user,
            # product=self.request.user.cart.products,
        )
