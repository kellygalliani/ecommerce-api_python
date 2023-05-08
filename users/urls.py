from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView

@extend_schema(
    summary="Login",
    description="This endpoint allows you to login and obtain a JWT token pair.",
    tags=["Login"]
)
class LoginView(TokenObtainPairView):
    pass

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<uuid:pk>/", views.UserDetailView.as_view()),
    path("users/<uuid:pk>/seller", views.UserDetailView.as_view()),
    path("users/login/", LoginView.as_view()),
]
