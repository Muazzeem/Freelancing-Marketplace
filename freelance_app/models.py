from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import gettext_lazy as _


class User(AbstractUser):
    class UserType(models.TextChoices):
        CLIENT = "Client", _("Client")
        ADMIN = "Freelancer", _("Freelancer")
        SUPERUSER = "Admin", _("Admin")
    role = models.CharField(max_length=10, choices=UserType.choices, default=UserType.CLIENT)
    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["email"]


class Job(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    created_by = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        def __str__(self):
            return self.title
        ordering = ['-created_at']