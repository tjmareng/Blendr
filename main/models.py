from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField()
    name = models.CharField(max_length=50)
    password = models.CharField(max_length=30)
