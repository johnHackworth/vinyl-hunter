from album.models import Album
from django.conf import settings
from artist.mocks import ArtistTestCaseFactory


class AlbumsTestCaseFactory:
    artist_factory = ArtistTestCaseFactory()

    number_of_albums = 0

    def __init__(self):
        self.newArtist()

    def newArtist(self):
        self.artist = self.artist_factory.persistedArtist()

    def album(self):
        album = Album()
        album.title = "irrelevant title"
        album.artist = self.artist
        album.ASIN = str(self.number_of_albums)
        album.URL = "http://"+str(self.number_of_albums)
        album.currentPrice = 1000
        album.minPrice = 1000
        album.thumbnail = str(self.number_of_albums)
        album.image = str(self.number_of_albums)
        album.priceUpdated = False
        album.availability = 'now'
        album.format = 'Test'

        self.number_of_albums += 1
        return album

    def persistedAlbum(self):
        album = self.album()
        album.artist.save() #WTF? without saving the artist again, it crashes
        album.save()
        return album
