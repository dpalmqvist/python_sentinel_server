from django.db import models
from django.contrib.auth.models import User

# Create your models here.
from django.urls import reverse


class MacIdentity(models.Model):
    mac = models.CharField(max_length=50)
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return "MacIdentity %s, %s, %s"%(self.mac, self.name, self.user)
    def get_absolute_url(self):
        return reverse('mac_identity', kwargs={'pk': self.pk})

class SentinelIdentity(models.Model):
    mac = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=200)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    def __str__(self):
        return "SentinelIdentity %s, %s, %s"%(self.mac, self.name, self.user)
    def get_absolute_url(self):
        return reverse('sentinel_identity', kwargs={'pk': self.pk})

class Detection(models.Model):
    sender = models.CharField(max_length=50)
    receiver = models.CharField(max_length=50)
    sentinel = models.CharField(max_length=50)
    sentinel_identity = models.ForeignKey(SentinelIdentity, on_delete=models.SET_NULL, null=True)
    sequence = models.IntegerField()
    rssi = models.FloatField()
    timestamp = models.DateField(auto_now_add=True)

