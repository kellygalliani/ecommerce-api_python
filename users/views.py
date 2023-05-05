from django.shortcuts import render
from .models import User
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import UserSerializer
from rest_framework import generics
from drf_spectacular.utils import extend_schema
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from .permissions import IsAccountOwnerOrAdmin

class UserView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get_permissions(self):
            if self.request.method =='POST':
                return [AllowAny()]
            return super().get_permissions()

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return User.objects.all()
        else: 
             user_id = self.request.user.id
             return queryset.filter(id=user_id)
    

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwnerOrAdmin]