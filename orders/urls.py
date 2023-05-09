from django.urls import path
from . import views

urlpatterns = [
    path("orders/<int:pk>/", views.OrderDetailView.as_view()),
    path("users/orders/", views.OrderView.as_view()),
    path("users/orders/buying/", views.BuyedOrderView.as_view()),
    path("users/orders/selling/", views.SellingOrderView.as_view()),
]
