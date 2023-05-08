from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.exceptions import NotFound
from orders.models import Order, OrderProducts
from orders.serializers import OrderSerializer
from .permissions import IsOrderSellerOrAdmin, IsSeller
<<<<<<< HEAD

=======
from drf_spectacular.utils import extend_schema
from django.shortcuts import get_object_or_404

@extend_schema(
    summary="Orders Routes",
    description="This endpoint allows you to list and create a order.",
    tags=["List and Create a Order"]
)
>>>>>>> 08166c710ac77f59dd69977973c23a39d326deb5

class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


@extend_schema(
    summary="Orders Routes",
    description="This endpoint allows you to update a order.",
    tags=["Update a Order"]
)

class OrderDetailView(generics.UpdateAPIView):
    permission_classes = [IsOrderSellerOrAdmin]
    authentication_classes = [JWTAuthentication]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
        order = OrderProducts.objects.filter(order_id=self.kwargs['pk']).first()

        if not order:
            raise NotFound()

        return super().get_object()
    
    def partial_update(self, request, *args, **kwargs):
        kwargs['partial'] = True
        return super().partial_update(request, *args, **kwargs)
    

class BuyedOrderView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Order.objects.filter(user_id=user_id)
        return queryset
    

class SellingOrderView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated, IsSeller]

    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Order.objects.filter(
            product__seller_id=user_id
        )
        return queryset
