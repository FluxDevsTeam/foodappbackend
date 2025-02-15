from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from rest_framework_simplejwt.tokens import RefreshToken


class UserManager(BaseUserManager):
    """
    Custom manager for the User model where email is the unique identifier.
    """

    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        if password:
            user.set_password(password)
        else:
            raise ValueError("Password must be provided")
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        """
        Create and return a regular user.
        """
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        """
        Create and return a superuser.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if not extra_fields['is_staff']:
            raise ValueError("Superuser must have is_staff=True.")
        if not extra_fields['is_superuser']:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


class User(AbstractUser):
    """
    Custom user model where email is the unique identifier for authentication.
    """
    username = None
    email = models.EmailField(unique=True)
    is_verified = models.BooleanField(default=False)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    otp = models.IntegerField(null=True)
    otp_created_at = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'  # Use email as the unique identifier
    REQUIRED_FIELDS = []  # No additional required fields

    objects = UserManager()

    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return ({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })

    def __str__(self):
        return self.email
