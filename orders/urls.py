from django.urls import path
from . import views

urlpatterns = [
    path("users/orders/", views.OrderView.as_view()),
    path("orders/<int:pk>/", views.OrderDetailView.as_view())
]
