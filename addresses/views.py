from rest_framework import generics
from rest_framework_simplejwt.authentication import JWTAuthentication

from .permissions import IsAccountOwnerOrAdmin
from .models import Address
from .serializers import AddressSerializer

class AddressUpdateView(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwnerOrAdmin]

    