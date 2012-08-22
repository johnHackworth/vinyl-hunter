from user_session.models import User
from commons.exceptions import InvalidPasswordException, InvalidFieldsException, ExistingEmailException, ExistingLoginException
from django.conf import settings
import crypt
import json


class User_service():


    def findUser(self, *args, **kwargs):
        users = User.objects.filter(**kwargs)
        if len(users) > 0:
            return users[0]
        else:
            return None

    def userSessionInfo(self, user, session):
        userDict = user.as_dict()
        userDict['session'] = session.as_dict(["id", "hash"])
        return json.dumps(userDict)

    def saveUser(self, user):
        try:
            user.validate()
        except InvalidFieldsException as invalidFields:
            raise invalidFields

        sameEmailUsers = User.objects.filter(email=user.email)
        for sameEmailUser in sameEmailUsers:
            if user.id != sameEmailUser.id:
                raise ExistingEmailException(user.email)

        sameLoginUsers = User.objects.filter(login=user.login)
        for sameLoginUser in sameLoginUsers:
            if user.id != sameLoginUser.id:
                raise ExistingLoginException(user.login)

        user.save()
        return user

    def assignPassword(self, user, old_password, new_password):
        if user.id is None or user.password == crypt.crypt(old_password, settings.PASSWORD_SALT):
            user.password = crypt.crypt(new_password, settings.PASSWORD_SALT)
            return user
        else:
            raise InvalidPasswordException(old_password)


