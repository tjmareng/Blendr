from django.db import models


# Create your models here.
class UserCard(models.Model):
    username = models.CharField(max_length=50)
    birthday = models.CharField(max_length=10)
    biography = models.TextField()
    gender = models.CharField(max_length=6)
    iso = models.CharField(max_length=6)
    email = models.CharField(max_length=50)
    age = models.CharField(max_length=5)

    def __str__(self):
        return self.email + ',' + self.username + ',' + self.biography + ',' + self.gender + ',' + self.iso + ',' + self.birthday