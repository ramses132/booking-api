from django.contrib.auth.models import AbstractUser
from django.contrib.auth.base_user import BaseUserManager
from django.utils.translation import gettext_lazy as _

from django.db import models
# from django.db import models


class UserManager(BaseUserManager):
    """
    Custom user model manager where email is the unique identifiers
    for authentication instead of usernames.
    """

    def create_user(self, email, password, **extra_fields):
        """
        Create and save a User with the given email and password.
        """
        if not email:
            raise ValueError(_('The Email must be set'))
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        """
        Create and save a SuperUser with the given email and password.
        """
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('is_active', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError(_('Superuser must have is_staff=True.'))
        if extra_fields.get('is_superuser') is not True:
            raise ValueError(_('Superuser must have is_superuser=True.'))
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    BUSINESS = "BUSINESS"
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    ROLE_CHOICES = (
        (BUSINESS, _("business")),
        (CUSTOMER, _("customer")),
        (ADMIN, _("administration")),
    )
    username = None
    role = models.CharField(verbose_name=_("role"), max_length=10, choices=ROLE_CHOICES)
    email = models.EmailField(_("email address"), blank=True, unique=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    objects = UserManager()

    def __str__(self):
        return self.email

class Room(models.Model):
    name = models.CharField(verbose_name=_("name"), max_length=64)
    capacity = models.PositiveIntegerField(_("capacity"), default=0)


    def __str__(self):
        return f"{self.name} | {self.capacity}"

class Event(models.Model):
    PUBLIC = "PUBLIC"
    PRIVATE = "PRIVATE"
    EVENT_TYPE_CHOICES = (
        (PUBLIC, _("public")),
        (PRIVATE, _("private")),
    )
    name = models.CharField(verbose_name=_("name"), max_length=64)
    date = models.DateField(verbose_name=_("date"))
    room = models.ForeignKey("booking.Room", verbose_name=_("room"), on_delete=models.CASCADE, related_name="events")
    event_type = models.CharField(max_length=10, default=PUBLIC, choices=EVENT_TYPE_CHOICES)

    def __str__(self):
        return f"{self.name} | {self.date} ({self.event_type})"


class Book(models.Model):
    event = models.ForeignKey("booking.Event", verbose_name=_("event"), on_delete=models.CASCADE, related_name="books")
    customer = models.ForeignKey("booking.User", verbose_name=_("customer"), on_delete=models.CASCADE, related_name="books")

    def __str__(self):
        return f"{self.event} | {self.customer}"
