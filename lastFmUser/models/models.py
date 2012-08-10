from django.db import models
from commons.models import ExtModel
from artist.models.models import Artist
from datetime import datetime, timedelta
import pytz

class LastFm_user(ExtModel, models.Model):

    name = models.CharField(max_length=255, default='', primary_key=True)
    lastFetched = models.DateTimeField(default=(datetime.now(pytz.utc) - timedelta(2)))
    artists = models.ManyToManyField(Artist)

    fields = ["id", "name", "lastFetched"]

    class Meta:
        app_label = 'lastFmUser'
        db_table = 'lastFmUsers'
