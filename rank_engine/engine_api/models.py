from django.db import models
from django.utils import timezone

import datetime


class Project(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    last_refresh = models.DateTimeField(default=timezone.now)
    ipfs = models.CharField(max_length=200, default="")
    abi = models.CharField(max_length=10000, default="")
    address = models.CharField(max_length=200, default="")
    count = models.IntegerField(default=0)
    banner_link = models.CharField(max_length=1000)
    total_supply = models.IntegerField()
    volume = models.IntegerField()


    def __str__(self):
        return self.name

# Create your models here.
