from django.db import models
from commons.models import ExtModel
from artist.models.models import Artist
from datetime import datetime


class LastFm_user(ExtModel, models.Model):

    name = models.CharField(max_length=255, default='', primary_key=True)
    lastFetched = models.DateTimeField(default=datetime(2001,1,1,1,1,1,1))
    artists = models.ManyToManyField(Artist)

    fields = ["id", "name", "lastFetched"]

    class Meta:
        app_label = 'lastFmUser'
        db_table = 'lastFmUsers'
