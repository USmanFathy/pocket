from django.db import models
from django.contrib.auth.models import AbstractUser
from .manager import UserManager
import uuid

class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True)
    reference = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    email_verified = models.BooleanField(default=False)
    email_token = models.CharField(max_length=100, null=True, blank=True)
    email_token_time = models.DateTimeField(null=True,blank=True)
    forgot_password = models.CharField(max_length=100, null=True, blank=True)
    forgot_password_time = models.DateTimeField(null=True,blank=True)
    otp_token = models.CharField(max_length=64,blank=True,null=True)
    otp_created = models.DateTimeField(null=True,blank=True)
    last_login = models.DateField(null=True,blank=True)
    last_logout = models.DateField(null=True,blank=True)
    created_on = models.DateField(auto_now_add=True)

    objects = UserManager()

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = []