from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path("users/", views.UserView.as_view()),
    path("users/<uuid:pk>/", views.UserDetailView.as_view()),
    path("users/<uuid:pk>/seller", views.UserDetailView.as_view()),
    path("users/login/", TokenObtainPairView.as_view()),
]
