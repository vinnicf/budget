from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.validators import RegexValidator


class CustomUser(AbstractUser):
        age = models.PositiveIntegerField(null=True, blank=True)

        phone_regex = RegexValidator(
        regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
        message="Phone number must be entered in the format: '(99) 99999-9999'. Up to 15 digits allowed.")
        phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True,)
        state = models.CharField(max_length=2, default='RS',)

        is_standard = models.BooleanField(default=True)
        is_premium = models.BooleanField(default=False)
