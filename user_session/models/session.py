from django.db import models
from commons.models import ExtModel
from user_session.models import User
from datetime import datetime
import pytz


class Session(ExtModel, models.Model):

    id = models.IntegerField(primary_key=True)
    # user = models.ForeignKey(User)
    hash = models.CharField(max_length=255, default='')
    created = models.DateTimeField(default=(datetime.now(pytz.utc)))
    lastChecked = models.DateTimeField(default=(datetime.now(pytz.utc)))

    fields = ["id", "user", "hash", "created", "lastChecked"]

    class Meta:
        app_label = 'user_session'
        db_table = 'user_sessions'
