from django.db import models
from commons.models import ExtModel
from datetime import datetime, timedelta
from artist.models import Artist
import pytz

class Album(ExtModel, models.Model):

    title = models.CharField(max_length=255, default='')
    lastFetched = models.DateTimeField(default=(datetime.now(pytz.utc)- timedelta(2)))
    artist = models.ForeignKey(Artist)
    ASIN = models.CharField(max_length = 16, unique = True, primary_key=True)
    currentPrice = models.DecimalField(decimal_places=2, max_digits=16, default=0.00)
    currency = models.CharField(max_length = 16, unique =False, default="USD")
    minPrice = models.DecimalField(decimal_places=2, max_digits=16, default=0.00)
    URL = models.CharField(max_length = 255, unique = True)
    thumbnail = models.CharField(max_length = 255, null=True, blank=True)
    image = models.CharField(max_length = 255, null=True, blank=True)
    priceUpdated = models.BooleanField(default=False)
    availability = models.CharField(max_length=128, default='now')
    format = models.CharField(max_length=32, null=True, blank=True, default=None)

    fields = ["title", "currentPrice", "currency","artist", "ASIN", "URL", "thumbnail", "minPrice", "format"]

    class Meta:
        app_label = 'album'
        db_table = 'albums'
