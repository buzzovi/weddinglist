from django.utils.translation import gettext_lazy as _
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.db.models import Value
from django.db.models.functions import Concat

from weddinglist.managers import UserManager


class User(AbstractUser):
    """User model.
    Username is replaced by email address for login.
    """
    username = None
    id = models.AutoField(primary_key=True)
    email = models.EmailField(_('email address'), unique=True)
    is_active = models.BooleanField(default=False)
    created = models.DateTimeField(auto_now_add=True, null=True, blank=True)
    modified = models.DateTimeField(auto_now=True, null=True, blank=True)

    # Email authentication Username field switch to email
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = UserManager()

    class Meta:
        verbose_name = "user"

    def full_name(self):
        return self.first_name + ' ' + self.last_name

    full_name.admin_order_field = Concat('first_name', Value(' '), 'last_name')
