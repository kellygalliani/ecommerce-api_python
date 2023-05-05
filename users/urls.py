from django.urls import path
from . import views
from rest_framework_simplejwt import views as jwt_views
from drf_spectacular.utils import extend_schema
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<int:pk>/", views.UserDetailView.as_view()),
    path("users/<int:pk>/seller", views.UserDetailView.as_view()),
    path("users/login/", TokenObtainPairView.as_view()),
]
