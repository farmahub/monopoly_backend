import uuid

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    PermissionsMixin,
    UserManager,
    Group,
    Permission,
)


class CustomUserManager(UserManager):
    def _create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("You have not specified a valid email")

        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self.db)

        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", "False")
        extra_fields.setdefault("is_superuser", "False")

        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", "True")
        extra_fields.setdefault("is_superuser", "True")

        return self._create_user(email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=255, blank=True, null=True, unique=True)
    avatar = models.ImageField(upload_to="avatars", blank=True, null=True)

    first_name = models.CharField(max_length=255, blank=True, null=True)
    last_name = models.CharField(max_length=255, blank=True, null=True)

    friends = models.ManyToManyField("self", blank=True)
    friends_count = models.IntegerField(default=0)

    is_active = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    date_joined = models.DateTimeField(auto_now_add=True)
    last_login = models.DateTimeField(blank=True, null=True)

    groups = models.ManyToManyField(
        Group,
        related_name="account_user_groups",  # Unique related name
        blank=True,
    )

    user_permissions = models.ManyToManyField(
        Permission,
        related_name="account_user_permissions",  # Unique related name
        blank=True,
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    EMAIL_FIELD = "email"
    REQUIRED_FIELDS = []

    def get_avatar(self):
        if self.avatar:
            return settings.WEBSITE_URL + self.avatar.url
        else:
            return "https://picsum.photos/200/200"


class FriendshipRequset(models.Model):
    STATUS_CHOICE = [
        ('sent', 'Sent'),
        ('accepted', 'Accepted'),
        ('rejeted', 'Rejected'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_for = models.ForeignKey(User, on_delete=models.CASCADE, related_name="recieved_request")
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name="created_request")
    status = models.CharField(max_length=10, choices=STATUS_CHOICE, default='sent')