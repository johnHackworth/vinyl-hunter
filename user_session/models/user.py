from django.db import models
from commons.models import ExtModel
from commons.exceptions import InvalidFieldsException
from lastFmUser.models import LastFm_user
from artist.models import Artist
from datetime import datetime
import pytz
from django.core.validators import email_re


class User(ExtModel, models.Model):

    # id = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255, default='')
    lastname = models.CharField(max_length=255, default='')
    login = models.CharField(max_length=255, default=None)
    password = models.CharField(max_length=255, default=None)
    email = models.CharField(max_length=255, default=None)
    location = models.CharField(max_length=255)
    country = models.IntegerField(max_length=3, default=1)
    gender = models.IntegerField(max_length=1, default=1)
    birthday = models.DateField(default="2001-01-01")
    creationDate = models.DateField(auto_now=True, auto_now_add=True)
    lastLogin = models.DateTimeField(default=str(datetime.now(pytz.utc)))
    about = models.CharField(max_length=1024)
    language = models.IntegerField(max_length=3, default=0)
    lastFmUser = models.ForeignKey(LastFm_user, null=True, default=None)
    artists = models.ManyToManyField(Artist, related_name='user_artists',symmetrical=False)
    ignoredArtists = models.ManyToManyField(Artist, related_name='ignored_artists',symmetrical=False)


    fields = ["id", "name", "lastname", "login", "email", "location", "country", "gender", "about", "language"]

    class Meta:
        app_label = 'user_session'
        db_table = 'users'

    def as_dict(self, fields=None):
        dictionary = super(User, self).as_dict(fields)
        return dictionary

    def validate(self):
        invalidFields = []
        if self.login is None or len(self.login) < 4:
            invalidFields.append('login')
        if self.password is None or len(self.password) < 4:
            invalidFields.append('password')
        if self.email is None:
            invalidFields.append('email')
        if not email_re.match(self.email):
            invalidFields.append('email')
        if len(invalidFields) > 0:
            raise InvalidFieldsException(invalidFields)

