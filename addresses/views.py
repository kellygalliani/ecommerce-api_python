from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication
from .permissions import IsAccountOwnerOrAdmin
from .models import Address
from .serializers import AddressSerializer
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Address Route",
    description="This endpoint allows you to update an address.",
    tags=["Update an Address"]
)
class AddressUpdateView(generics.UpdateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwnerOrAdmin]

    queryset = Address.objects.all()
    serializer_class = AddressSerializer
