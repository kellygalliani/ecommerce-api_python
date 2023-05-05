from django.shortcuts import render
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from users.permissions import IsAccountOwnerOrAdmin
from .models import Address
from .serializers import AddressSerializer
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import AnonymousUser
from rest_framework.exceptions import NotAuthenticated

class AddressUpdateView(generics.UpdateAPIView):
    queryset = Address.objects.all()
    serializer_class = AddressSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwnerOrAdmin]
    
    def get_queryset(self):
        if not self.request.user.is_authenticated:
            raise NotAuthenticated("Authentication credentials were not provided.")
        return Address.objects.filter(pk=self.kwargs["pk"], user=self.request.user)

    