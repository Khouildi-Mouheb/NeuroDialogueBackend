from django.db import models
from django.contrib.auth.models import AbstractBaseUser , PermissionsMixin
from .managers import UserManager
import uuid


class User(AbstractBaseUser , PermissionsMixin):
    id=models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False,
    )
    email=models.EmailField(
        unique=True
        )
    firstName=models.CharField(
        max_length=20
        )
    lastName=models.CharField(
        max_length=20
        )

    is_active=models.BooleanField(
        default=True
        )
    is_staff=models.BooleanField(
        default=True
        )
    dateJoined=models.DateTimeField(
        auto_now_add=True
        )
    image=models.ImageField(
        blank=True,
        null=True,
        )
    
    objects=UserManager()
    USERNAME_FIELD="email"
    REQUIRED_FIELDS=['firstName','lastName']

    def __str__(self):
        return f"{self.email}"