from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.exceptions import NotFound
from orders.models import Order, OrderProducts
from orders.serializers import OrderSerializer
from .permissions import IsOrderSellerOrAdmin, IsSeller
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Orders Routes",
    description="This endpoint allows you to list and create an order.",
    tags=["List and Create an Order"]
)

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
    description="This endpoint allows you to update an order.",
    tags=["Update an Order"]
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

@extend_schema(
    summary="Order Routes",
    description="This endpoint allows you to list all bought products.",
    tags=["List Bought Products"]
)

class BuyedOrderView(generics.ListAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def get_queryset(self):
        user_id = self.request.user.id
        queryset = Order.objects.filter(user_id=user_id)
        return queryset
    
@extend_schema(
    summary="Order Routes",
    description="This endpoint allows you to list all your sales.",
    tags=["List Sales"]
)

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
