from django.contrib.auth.models import AbstractUser
from django.db import models

# Create your models here.

class CustomUser(AbstractUser):
        age = models.PositiveIntegerField(null=True, blank=True)
        is_standard = models.BooleanField(default=True)
        is_premium = models.BooleanField(default=False)
