from django.db import models
from django.contrib.auth.models import User


class UserProfile(models.Model):
    user    =models.OneToOneField(User , related_name = 'userprofile' , on_delete= models.CASCADE)
    balance = models.IntegerField()
    active  = models.BooleanField(default=False)
    code    = models.IntegerField(primary_key=True)