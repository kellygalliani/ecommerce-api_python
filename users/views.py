from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import AllowAny
from rest_framework import generics
from rest_framework.exceptions import NotFound, NotAcceptable

from orders.models import Order
from .serializers import UserSerializer
from .models import User
from .permissions import IsAccountOwnerOrAdmin
<<<<<<< HEAD
import uuid
=======

from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="List and create users",
    description="This endpoint allows you to list all users and create new ones.",
    tags=["List and Create Users"]
)
>>>>>>> 08166c710ac77f59dd69977973c23a39d326deb5

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
        try:
            valid_id = uuid.UUID(self.request.user.id, version=4)
        except ValueError:
             raise NotFound()

        queryset = super().get_queryset()
        if self.request.user.is_superuser:
            return User.objects.all()
        else: 
             user_id = self.request.user.id
             return queryset.filter(id=user_id)

<<<<<<< HEAD
=======
@extend_schema(
    summary="Retrieve, update and delete a user",
    description="This endpoint allows you to retrieve, update and delete a specific user.",
    tags=["Retrieve, update and delete a user"]
)
>>>>>>> 08166c710ac77f59dd69977973c23a39d326deb5

class UserDetailView(generics.RetrieveUpdateDestroyAPIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAccountOwnerOrAdmin]

    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_destroy(self, instance):
         found_in_done = Order.objects.filter(user_id=self.kwargs["pk"]).filter(order_status="PEDIDO REALIZADO").first()
         found_in_progress = Order.objects.filter(user_id=self.kwargs["pk"]).filter(order_status="EM ANDAMENTO").first()
         found_in_delivered = Order.objects.filter(user_id=self.kwargs["pk"]).filter(order_status="EM ANDAMENTO").first()
         
         if found_in_done or found_in_progress:
              raise NotAcceptable({"message": "This user has unfinished orders."})
         elif found_in_delivered:
              user = User.objects.get(id=self.request.user.id)
              user.is_active = False

         return super().perform_destroy(instance)
