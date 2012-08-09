from artist.models import Artist
from datetime import datetime
from lastFmUser.models import LastFm_user
from vendors.lastfmCrawler.lastfmSearch import Lastfm

class LastFm_user_service():


    def __init__(self, user_service):
        self.api = Lastfm()

    def fetchUser(self, username):
        lastFm_user = LastFm_user.objects.get_or_create(name=username)[0]

        self.api.fetch(username)
        for artist_data in self.api.artists:
            artist = Artist.objects.get_or_create(**artist_data)[0]
            lastFm_user.artists.add(artist)

        lastFm_user.lastFetched = datetime.now()
        lastFm_user.save()



