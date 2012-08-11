from artist.models import Artist
from datetime import datetime, timedelta
from lastFmUser.models import LastFm_user
from commons.exceptions import NotFoundException
from vendors.lastfmCrawler.lastfmSearch import Lastfm
from settings import LAST_FETCH_LIMIT
import pytz


last_fetch_limit = datetime.now(pytz.utc) - timedelta(LAST_FETCH_LIMIT)


class LastFm_user_service():

    def __init__(self, artists_service):
        self.api = Lastfm()
        self.artistsService = artists_service

    def fetchUser(self, lastFm_user):
        username = lastFm_user.name
        self.api.fetch(username)
        for artist_data in self.api.artists:
            artists = Artist.objects.filter(name=artist_data['name'])
            if len(artists) == 0:
                artist = Artist(**artist_data)
                artist.save()
            else:
                artist = artists[0]

            lastFm_user.artists.add(artist)

        lastFm_user.lastFetched = datetime.now(pytz.utc)
        lastFm_user.save()

    def updateUser(self, user):
        if user.lastFetched < last_fetch_limit:
            self.fetchUser(user)

    def updateUserByName(self, username):
        lastFm_user = LastFm_user.objects.get_or_create(name=username)[0]
        self.updateUser(lastFm_user)
        return lastFm_user

    def fetchUserArtists(self, user):
        for artist in user.artists.all():
            self.artistsService.updateArtistAlbums(artist)

    def fetchAll(self, username):
        lastFm_user = self.updateUserByName(username)
        self.fetchUserArtists(lastFm_user)
        return lastFm_user

    def getExportedArtists(self, user):
        exported_artists = []
        for artist in user.artists.all():
            exported_artists.append(artist.as_dict())
        return exported_artists

    def getUserAlbumsByName(self, username, max_price=None):
        lastFm_users = LastFm_user.objects.filter(name=username)
        if len(lastFm_users) == 0:
            # throw NotFoundException
            return None
        lastFm_user = lastFm_users[0]
        return self.getUserAlbums(lastFm_user, max_price)

    def getUserAlbums(self, lastFm_user, max_price=None):
        albums = []
        for artist in lastFm_user.artists.all():
            albums += (self.artistsService.getArtistAlbums(artist, max_price))
        return albums
