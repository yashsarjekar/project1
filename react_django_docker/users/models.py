from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# Create your models here.

class Permission(models.Model):
    name = models.CharField(max_length=200)

class Role(models.Model):
    name = models.CharField(max_length=200)
    permission = models.ManyToManyField(Permission)

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("The Email field must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractUser):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    email = models.CharField(max_length=200, unique=True)
    password = models.CharField(max_length=200)
    username = models.CharField(max_length=200)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()


   
