from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView
from drf_spectacular.utils import extend_schema

@extend_schema(
    summary="Login",
    description="This endpoint allows you to login and obtain a JWT token pair.",
    tags=["Login"]
)
class LoginView(TokenObtainPairView):
    pass

urlpatterns = [
    path("users/login/", LoginView.as_view()),
    path("users/", views.UserView.as_view()),
    path("users/<str:pk>/", views.UserDetailView.as_view()),
    path("users/<str:pk>/seller/", views.UserDetailView.as_view()),
    path("users/activate/<str:pk>/", views.UserActivateView.as_view())
]
