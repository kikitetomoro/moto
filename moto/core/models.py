from django.contrib.auth.models import AbstractUser
from django.db import models
from item.models import *
class CustomUser(AbstractUser):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    USER_STATUS_CHOICES = (
        ('corporate', '保護団体'),
        ('individual', '個人'),
    )
    userstatus = models.CharField(max_length=20, choices=USER_STATUS_CHOICES)
    def __str__(self):
        return self.username
    
    def liked_items(self):
        return self.item_liked_items.all()