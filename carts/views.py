from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from addresses.permissions import IsAccountOwnerOrAdmin
from drf_spectacular.utils import extend_schema
from .models import Cart
from .serializers import CartSerializer, CartClearSerializer

@extend_schema(
    summary="Cart Routes",
    description="This endpoint allows you to create and a cart.",
    tags=["Create and Update a Cart"]
)

class CartView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    lookup_field = 'product_id'
    serializer_class = CartSerializer

    def get_object(self):
        return Cart.objects.get(user=self.request.user)
    
    def perform_update(self, serializer):
        products = self.kwargs.get('product_id')
        if not products:
            raise NotFound()

        quantity = self.request.data
        serializer.save(user=self.request.user, products=products, context=quantity)

@extend_schema(
    summary="Cart Routes",
    description="This endpoint allows you to clean a cart.",
    tags=["Clean a Cart"]
)
class CartClearView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwnerOrAdmin]

    queryset = Cart.objects.all()
    serializer_class = CartClearSerializer
    lookup_field = 'id'
