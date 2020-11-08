from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SubType(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    color = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    subType = models.OneToOneField(
        SubType, on_delete=models.CASCADE)

    def __str__(self):
        return self.subType.name


class Video(models.Model):
    title = models.CharField(max_length=100)
    ytId = models.CharField(max_length=100)
    subType = models.ForeignKey(
        SubType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title
