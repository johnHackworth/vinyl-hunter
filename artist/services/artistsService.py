from artist.models import Artist
from album.models import Album
from datetime import datetime, timedelta
from vendors.amazonProductApiCrawler.amazonSearch import Amazon
import pytz


class Artists_service():

    def __init__(self):
        self.api = Amazon()

    def fetchArtist(self, artist):
        self.api.fetch(artist.name)
        for album_data in self.api.albums:

            album_data['artist'] = artist
            currentPrice = album_data.pop('price')

            albums = Album.objects.filter(ASIN=album_data['ASIN'])
            if len(albums) == 0:
                album = Album(**album_data)
            else:
                album = albums[0]

            album.currentPrice = currentPrice
            album.lastFetched = datetime.now(pytz.utc)
            if album.minPrice == 0.00 or album.minPrice > album.currentPrice:
                album.minPrice = album.currentPrice
                album.priceUpdated = True
            else:
                album.priceUpdated = False
            album.save()


        artist.lastFetched = datetime.now(pytz.utc)
        artist.save()

    def updateArtistAlbums(self, artist):
        yesterday =  datetime.now(pytz.utc) - timedelta(1)
        if artist.lastFetched < yesterday:
            self.fetchArtist(artist)

    def updateArtistAlbumsByName(self, name):
        artist = Artist.objects.get_or_create(name=name)[0]
        self.updateArtistAlbums(artist)




