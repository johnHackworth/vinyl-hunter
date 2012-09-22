from user_session.models import User
from commons.exceptions import InvalidPasswordException, InvalidFieldsException, ExistingEmailException, ExistingLoginException
from django.conf import settings
import crypt
import json


class User_service():

    def __init__(self, lastFm_user_service = None):
        self.lastFm_service = lastFm_user_service

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

    def saveUser(self, user, update = False):
        try:
            user.validate()
        except InvalidFieldsException as invalidFields:
            raise invalidFields

        if not update:
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

        if (user.id is None or user.password == crypt.crypt(old_password, settings.PASSWORD_SALT) )and new_password is not None:
            user.password = crypt.crypt(new_password, settings.PASSWORD_SALT)
            return user
        else:
            raise InvalidPasswordException(old_password)

    def createUser(self):
        user = User()
        return user

    def assignLastFmUser(self, user, lastFm_user):
        user.lastFmUser = lastFm_user
        user.save()
        self.importArtistsFromLastFmUser(user)

    def searchAndAssignLastFmUser(self, user, lastFm_name):
        lastFm_user = self.lastFm_service.fetchAll(lastFm_name)
        self.assignLastFmUser(user, lastFm_user)

    def importArtistsFromLastFmUser(self, user):
        if user.lastFmUser is not None:
            for artist in user.lastFmUser.artists.all():
                user.artists.add(artist)

    def addArtist(self, user, artist_name):
        artist = self.lastFm_service.getArtist(artist_name)
        if artist is not None:
            user.artists.add(artist)
        return artist

    def ignoreArtist(self, user, artist_name):
        artist = self.lastFm_service.getArtist(artist_name)
        if artist is not None:
            user.ignoredArtists.add(artist)
        return artist

    def removeIgnoredArtist(self, user, artist_name):
        artist = self.lastFm_service.getArtist(artist_name)
        if artist is not None:
            user.ignoredArtists.remove(artist)
        return artist

    def getUserArtists(self, user):
        not_ignored_artists = []
        for artist in user.artists.all():
            if artist not in user.ignoredArtists.all():
                not_ignored_artists.append(artist)
        return not_ignored_artists

    def getExportedArtists(self, user):
        exported_artists = []
        for artist in self.getUserArtists(user):
                exported_artists.append(artist.as_dict())
        return exported_artists

    def getUserAlbums(self, user, max_price=None, filter_singles = False, currency=None):
        albums = []
        for artist in self.getUserArtists(user):
            albums += (self.lastFm_service.artistsService.getArtistAlbums(artist, max_price, bool(filter_singles), currency))
        return albums

