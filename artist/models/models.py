from django.db import models
from commons.models import ExtModel
from datetime import datetime, timedelta
import pytz

class Artist(ExtModel, models.Model):

    name = models.CharField(max_length=255, default='', primary_key=True)
    lastFetched = models.DateTimeField(default=(datetime.now(pytz.utc) - timedelta(2)))
    thumbnail = models.CharField(max_length=255, default='')
    image = models.CharField(max_length=255, default='')
    largeImage = models.CharField(max_length=255, default='')

    fields = ["name", "lastFetched", "thumbnail", "image", "largeImage"]

    class Meta:
        app_label = 'artist'
        db_table = 'artists'
