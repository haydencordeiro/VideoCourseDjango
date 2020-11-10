from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class SubType(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    color = models.CharField(max_length=100)
    discountPrice = models.IntegerField(default=0)

    def __str__(self):
        return self.name


class Subscription(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    subType = models.OneToOneField(
        SubType, on_delete=models.CASCADE)
    date = models. DateTimeField(auto_now=True)

    def __str__(self):
        return self.subType.name


class Video(models.Model):
    title = models.CharField(max_length=100)
    ytId = models.CharField(max_length=1000)
    desc = models.CharField(max_length=100, default="")
    subType = models.ForeignKey(
        SubType, on_delete=models.CASCADE)

    def __str__(self):
        return self.title


class TypeAccess(models.Model):
    subType = models.ForeignKey(
        SubType, on_delete=models.CASCADE, related_name="subType")
    canAccess = models.ForeignKey(
        SubType, on_delete=models.CASCADE, related_name="canAccess")


class Transations(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE)
    amount = models.IntegerField()
    date = models. DateTimeField(auto_now=True)
    success = models.BooleanField(default=False)
    paytmOID = models.CharField(max_length=100, default="")
    subType = models.ForeignKey(
        SubType, on_delete=models.CASCADE, null=True)


class Testimonials(models.Model):
    name = models.CharField(max_length=100)
    desc = models.CharField(max_length=1000)
