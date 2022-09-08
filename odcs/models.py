from asyncio.windows_events import NULL
from django.db import models
from django.db.models import Model
from django.contrib.auth.models import AbstractUser



# Overriding the Default Django Auth User and adding One More Field (user_type)
class CustomUser(AbstractUser):
    user_type_data = ((1, "admin"), (2, "employee"))
    user_type = models.CharField(default=1, choices=user_type_data, max_length=10)
    phoneNo = models.CharField(max_length=13)
    address = models.CharField(max_length=25)
    dateOfBirth = models.DateField(null=True)
    gender = models.CharField(max_length=5)