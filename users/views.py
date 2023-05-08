from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import generics
from .serializers import UserSerializer
from .models import User
from .permissions import IsAccountOwnerOrAdmin


class UserView(generics.ListCreateAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = User.objects.all()
    serializer_class = UserSerializer

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
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwnerOrAdmin]

    queryset = User.objects.all()
    serializer_class = UserSerializer
