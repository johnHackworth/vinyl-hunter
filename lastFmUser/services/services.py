from lastFmUser.models.models import LastFm_user
from artist.models.model import Artist
from vendors.lastfmCrawler.lastfmSearch import Lastfm

class LastFm_user_service():


    def __init__(self, user_service):
        self.api = Lastfm()

    def fetchUser(self, username):
        self.api.fetch(username)
        for artist in self.api.artists:


