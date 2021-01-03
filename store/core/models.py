from djongo import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.conf import settings


class UserManager(BaseUserManager):

    def create_user(self, email, password=None, **extra_fields):
        """Creates and save a new user"""
        if not email:
            raise ValueError('User must have an username')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save()

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new super user"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save()

        return user


class User(AbstractBaseUser, PermissionsMixin, models.Model):
    """Custom user model that support using email instead of username"""
    username = None
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []


class Stores(models.Model):
    """Collections of the all store info"""
    store_id = models.AutoField(primary_key=True)
    store_name = models.CharField(max_length=255)
    store_type = models.CharField(max_length=255)
    store_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return self.store_name


class Products(models.Model):
    """Each single product information"""
    product_id = models.AutoField(primary_key=True)
    product_name = models.CharField(max_length=255)
    product_price = models.FloatField(max_length=10)
    product_type = models.CharField(max_length=255)
    connected_container_id = models.OneToOneField('ProductContainer', on_delete=models.CASCADE)

    def __str__(self):
        return self.product_name


class ProductContainer(models.Model):
    """Each single product information"""
    container_id = models.AutoField(primary_key=True)
    store_id = models.OneToOneField('Stores', on_delete=models.CASCADE)
    container_owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return str(self.container_id)
