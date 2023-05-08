from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import generics
from rest_framework.exceptions import NotFound
from orders.models import Order, OrderProducts
from orders.serializers import OrderSerializer
from .permissions import IsOrderSellerOrAdmin, IsSeller


class OrderView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    serializer_class = OrderSerializer

    def perform_create(self, serializer):
        serializer.save(
            user=self.request.user
        )


class OrderDetailView(generics.UpdateAPIView):
    permission_classes = [IsOrderSellerOrAdmin]
    authentication_classes = [JWTAuthentication]

    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def get_object(self):
        order = OrderProducts.objects.get(order_id=self.kwargs['pk'])

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
