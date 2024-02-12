from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import RegexValidator


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, username=email, **extra_fields) 
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    
        age = models.PositiveIntegerField(null=True, blank=True)
        email = models.EmailField(unique=True)
        phone_regex = RegexValidator(
        regex=r'^\(\d{2}\) \d{4,5}-\d{4}$',
        message="Phone number must be entered in the format: '(99) 99999-9999'. Up to 15 digits allowed.")
        phone_number = models.CharField(validators=[phone_regex], max_length=17, null=True,)
        state = models.CharField(max_length=2, default='RS',)

        is_standard = models.BooleanField(default=True)
        is_premium = models.BooleanField(default=False)

        objects = CustomUserManager()

        USERNAME_FIELD = 'email'
        REQUIRED_FIELDS = []  # Remove 'email' from REQUIRED_FIELDS

        def __str__(self):
                return self.email
