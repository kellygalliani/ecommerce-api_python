from django.shortcuts import render
from rest_framework import generics
from carts.models import Cart
from orders.models import Order
from rest_framework.views import Response, status
from .permissions import IsOrderSellerOrAdmin
from orders.serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from users.models import User
import ipdb
from rest_framework_simplejwt.authentication import JWTAuthentication


class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]
    serializer_class = OrderSerializer


    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class OrderDetailView(generics.UpdateAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [IsOrderSellerOrAdmin]
    authentication_classes = [JWTAuthentication]
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().partial_update(request, *args, **kwargs)