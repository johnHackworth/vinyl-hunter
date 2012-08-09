from django.db import models
from commons.models import ExtModel
from artist.models.models import Artist


class LastFm_user(ExtModel, models.Model):

    name = models.CharField(max_length=255, default='')
    lastFetched = models.DateTimeField()
    artists = models.ManyToManyField(Artist)

    fields = ["id", "name", "lastFetched"]

    class Meta:
        app_label = 'lastFmUser'
        db_table = 'lastFmUsers'
