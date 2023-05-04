from django.db import models


class OrderStatusOptions(models.TextChoices):
    order_started = "PEDIDO REALIZADO"
    order_in_progess = "EM ANDAMENTO"
    delivered = "ENTREGUE"


class Order(models.Model):
    class Meta:
        ordering = ["id"]

    order_status = models.CharField(
        choices=OrderStatusOptions.choices,
        default=OrderStatusOptions.order_started,
    )
    total_price = models.DecimalField(
        max_digits=9, decimal_places=2, default=0.00
    )
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        "users.User", on_delete=models.PROTECT, related_name="orders"
    )
    product = models.ManyToManyField(
        "products.Product",
        related_name="order",
        through="orders.OrderProducts",
    )


class OrderProducts(models.Model):
    order = models.ForeignKey("orders.Order", on_delete=models.CASCADE)
    product = models.ForeignKey("products.Product", on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
