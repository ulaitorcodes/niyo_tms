
from typing import ClassVar

from django.contrib.auth.models import AbstractUser
from django.db.models import CharField
from django.db.models import EmailField
from django.urls import reverse
from django.utils.translation import gettext_lazy as _
from django.db import models
from .managers import UserManager


class User(AbstractUser):
  
   
    name = CharField(_("Name of User"), blank=True, max_length=255)
    first_name = CharField(_("First Name"), max_length=30, default="", blank=False,)  # Set blank=False to make it required
    last_name = CharField(_("Last Name"), max_length=150, default="", blank=False)  # Set blank=False to make it required
    email = EmailField(_("email address"), unique=True)
    photo = models.ImageField(upload_to='media/user/user_photos', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    username = None  
    

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects: ClassVar[UserManager] = UserManager()

    def get_absolute_url(self) -> str:
        """Get URL for user's detail view.

        Returns:
            str: URL for user detail.

        """
        return reverse("users:detail", kwargs={"pk": self.id})
