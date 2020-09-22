from django.utils.translation import gettext_lazy as _
from django.db import models


class GiftList(models.Model):
    """" Gift List
    """
    name = models.CharField(max_length=255, unique=True)
    owner = models.ForeignKey(
        'User', on_delete=models.SET_NULL, blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    # objects = models.Manager()

    class Meta:
        verbose_name = "Gift List"
        ordering = ['id']


class GiftListItem(models.Model):
    """" Gift List
    """

    STATUS = (
        ('available', _('available')),
        ('purchased', _('purchased')),
    )

    gift_list = models.ForeignKey(
        'GiftList', related_name="giftlist", on_delete=models.SET_NULL, blank=True, null=True)
    gift = models.ForeignKey(
        'Gift', related_name="gift", on_delete=models.SET_NULL, blank=True, null=True)
    payer = models.ForeignKey(
        'User', related_name="user", on_delete=models.SET_NULL, blank=True, null=True)
    status = models.CharField(
        max_length=9, choices=STATUS, default=STATUS[0][0])
    purchased_date = models.DateTimeField(null=True, blank=True)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    @property
    def price(self):
        return self.gift.price

    @property
    def gift_name(self):
        return self.gift.name

    @property
    def gift_brand(self):
        return self.gift.brand

    class Meta:
        verbose_name = "Gift List Item"
        ordering = ['id']
