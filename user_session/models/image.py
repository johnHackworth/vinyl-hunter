from django.db import models
from user_session.models import User
from datetime import datetime
import pytz


class Image(models.Model):
    url = models.CharField(max_length=640)
    user = models.Integeruser = models.ForeignKey(User)
    created = models.DateTimeField(default=(datetime.now(pytz.utc)))

    class Meta:
        app_label = 'user_session'
        db_table = 'user_images'
