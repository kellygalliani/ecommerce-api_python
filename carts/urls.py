from django.urls import path
from . import views

urlpatterns = [
    path("cart/product/<int:product_id>/", views.CartView.as_view())
]