from django.urls import path
from . import views

urlpatterns = [path("users/orders/", views.OrderView.as_view())]
