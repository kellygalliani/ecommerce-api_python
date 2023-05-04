from django.shortcuts import render
from rest_framework import generics

# Create your views here.
from orders.serializers import OrderSerializer
from rest_framework.permissions import IsAuthenticated


class OrderView(generics.ListCreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
