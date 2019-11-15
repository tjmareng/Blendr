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
    distance_from_current_user = models.CharField(max_length=50)
    city = models.CharField(max_length=100)
    coordinates = models.CharField(max_length=50)

    def __str__(self):
        return self.email + ',' + self.username + ',' + self.biography + ','\
               + self.gender + ',' + self.iso + ',' + self.birthday + ', '\
               + self.age + ',' + self.distance_from_current_user + ',' + self.city + ',' + self.coordinates
