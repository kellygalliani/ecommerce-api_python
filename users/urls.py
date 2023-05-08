from django.urls import path
from . import views
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
<<<<<<< HEAD
    path("users/<pk>/", views.UserDetailView.as_view()),
    path("users/<pk>/seller", views.UserDetailView.as_view()),
    path("users/login/", TokenObtainPairView.as_view()),
=======
    path("users/<uuid:pk>/", views.UserDetailView.as_view()),
    path("users/<uuid:pk>/seller", views.UserDetailView.as_view()),
    path("users/login/", LoginView.as_view()),
>>>>>>> 08166c710ac77f59dd69977973c23a39d326deb5
]
