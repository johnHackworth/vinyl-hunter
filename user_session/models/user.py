from django.db import models
from commons.models import ExtModel
from datetime import datetime
import pytz

class User(ExtModel, models.Model):

    name = models.CharField(max_length=255, default='')
    lastname = models.CharField(max_length=255, default='')
    login = models.CharField(max_length=255, default=None)
    password = models.CharField(max_length=255, default=None)
    email = models.CharField(max_length=255, default=None)
    location = models.CharField(max_length=255)
    country = models.IntegerField(max_length=3, default=1)
    gender = models.IntegerField(max_length=1, default=1)
    birthday = models.DateField(default="2001-01-01")
    creationdate = models.DateField(auto_now=True, auto_now_add=True)
    lastlogin = models.DateTimeField(default=str(datetime.now()))
    aboutme = models.CharField(max_length=1024)
    languaje = models.IntegerField(max_length=3, default=0)

    fields = ["id", "name", "lastname", "login", "email", "location", "country", "gender", "aboutme", "languaje"]

    class Meta:
        app_label = 'user_session'
        db_table = 'users'

    def as_dict(self, fields=None):
        dictionary = super(User, self).as_dict(fields)

        if self.image_id is not None and self.image_id > 0:
            imageObj = Image.objects.filter(id=self.image_id)
            if len(imageObj) > 0:
                dictionary['image_url'] = imageObj[0].url

        return dictionary

    def validate(self):
        invalidFields = []
        if self.login is None:
            invalidFields.append('login')
        if self.password is None:
            invalidFields.append('password')
        if self.email is None:
            invalidFields.append('email')
        if len(invalidFields) > 0:
            raise InvalidFieldsException(invalidFields)
