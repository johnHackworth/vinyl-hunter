from artist.models import Artist
from datetime import datetime
from lastFmUser.models import LastFm_user
from vendors.lastfmCrawler.lastfmSearch import Lastfm
import pytz


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

    def fetchUserByName(self, username):
        lastFm_user = LastFm_user.objects.get_or_create(name=username)[0]
        self.fetchUser(lastFm_user)

    def fetchUserArtists(self, user):
        for artist in user.artists.all():
            self.artistsService.updateArtistAlbums(artist)

    def fetchAll(self, username):
        lastFm_user = LastFm_user.objects.get_or_create(name=username)[0]
        self.fetchUser(lastFm_user)
        self.fetchUserArtists(lastFm_user)
        return lastFm_user

    def getExportedArtists(self, user):
        exported_artists = []
        for artist in user.artists.all():
            exported_artists.append(artist.as_dict())
        return exported_artists


