# from django.utils.translation import gettext_lazy as _
from django.db import models


class Gift(models.Model):
    """" Gift
    """
    name = models.CharField(max_length=255, unique=True)
    brand = models.CharField(max_length=255, null=True, blank=True)
    price = models.IntegerField(default=0)
    currency = models.CharField(
        default="GBP", null=True, blank=True, max_length=5)
    in_stock_quantity = models.IntegerField(default=0)
    info = models.TextField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    objects = models.Manager()

    class Meta:
        verbose_name = "Gift"
        ordering = ['id']
