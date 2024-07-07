from django.db import models

from django.contrib.auth.models import AbstractUser

# Create your models here.

#AbstracUser para agregar el campo 

class User(AbstractUser):
    ROLE_CHOICES = (
        ('operator', 'Operator'),
        ('supervisor', 'Supervisor'),
        ('admin', 'Administrator'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='operator')

    def __str__(self):
        return self.username