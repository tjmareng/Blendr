from django.db import models


# Create your models here.
class User(models.Model):
    email = models.EmailField()
    username = models.CharField(max_length=50)
    bio = models.TextField()
    sex = models.CharField(max_length=6)
    iso = models.CharField(max_length=6)

