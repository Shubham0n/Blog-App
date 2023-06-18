from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.conf import settings

class CustomManager(BaseUserManager):
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("The given email must be set")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("is_active", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractUser):
    role_choices = (
        ('Reader', 'Reader'),
        ('Bloger', 'Bloger'),
    )

    email = models.EmailField("email address", unique=True, max_length=256)
    first_name = models.CharField("first name", max_length=10, blank=True)
    last_name = models.CharField("last name", max_length=10, blank=True)
    date_of_birth = models.DateField("date of birth", null=True)
    is_active = models.BooleanField("active", default=True)
    is_staff = models.BooleanField("staff", default=False)
    is_superuser = models.BooleanField("superuser", default=False)
    is_role = models.CharField("who are you?", choices=role_choices, default="", max_length=10)
    is_reader = models.BooleanField("Reader", default=False)
    is_blogger = models.BooleanField("blogger", default=False)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    objects = CustomManager()

    def get_full_name(self):
        full_name = self.first_name + " " + self.last_name
        return full_name

    def __str__(self):
        return self.first_name + " " + self.last_name


class BlogsDetails(models.Model):
    blog_title = models.CharField(max_length=500, null=False)
    blog_date = models.DateField(auto_now_add=True, blank=False, null=False)
    blog_content = models.TextField(max_length=10000, null=False)
    created_by  = models.ForeignKey('CustomUser', on_delete=models.CASCADE)

    def __str__(self):
        return self.blog_title

class Comment(models.Model):
    comment = models.TextField(max_length=1000, null=False)
    comment_date = models.DateField(auto_now_add=True, blank=False, null=False)
    created_by = models.ForeignKey('CustomUser', on_delete=models.CASCADE)
    blog_title = models.ForeignKey('BlogsDetails', on_delete=models.CASCADE)

    def __str__(self):
        return self.comment