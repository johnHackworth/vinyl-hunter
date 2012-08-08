from django.db import models
from commons.models import ExtModel
from datetime import datetime


class Artist(ExtModel, models.Model):

    name = models.CharField(max_length=255, default='')
    lastFetched = models.DateTimeField()
    thumbnail = models.CharField(max_length=255, default='')
    image = models.CharField(max_length=255, default='')
    largeImage = models.CharField(max_length=255, default='')

    fields = ["id", "name", "lastFetched", "thumbnail", "image", "largeImage"]
