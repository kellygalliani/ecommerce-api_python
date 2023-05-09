from django.db import models


class Address(models.Model):

    street = models.CharField(max_length=255)
    number = models.CharField(max_length=50)
    po = models.CharField(max_length=20)
    city = models.CharField(max_length=50)
    country = models.CharField(max_length=50)
    state = models.CharField(max_length=50)
    complement = models.CharField(max_length=255, null=True, blank=True, default=None)
