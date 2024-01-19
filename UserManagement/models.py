from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin


class CustomUserManager(BaseUserManager):

    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError('Email fields is required!!')

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user
    
    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(
                    unique=True
                    )
    first_name = models.CharField(
                    verbose_name='First Name',
                    max_length=20
                    )
    last_name = models.CharField(
                    verbose_name='Last Name',
                    max_length = 20
                    )
    is_active = models.BooleanField(
                    default=True
                    )
    is_staff = models.BooleanField(
                    verbose_name='Staff',
                    default=False
                    )
    is_superuser = models.BooleanField(
                    verbose_name='SuperUser',
                    default=False
                    )
    is_buyer = models.BooleanField(
                    verbose_name='Buyer',
                    default=False
                    )
    is_seller = models.BooleanField(
                    verbose_name='Seller',
                    default=False
                    )

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self) -> str:
        return self.email



