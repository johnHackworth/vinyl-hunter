from artist.models import Artist
from album.models import Album
from datetime import datetime, timedelta
from vendors.amazonProductApiCrawler.amazonSearch import Amazon
from settings import LAST_FETCH_LIMIT
import pytz


last_fetch_limit = datetime.now(pytz.utc) - timedelta(LAST_FETCH_LIMIT)


class Artists_service():

    def __init__(self, albums_service=None):
        self.api = Amazon()
        self.albumsService = albums_service

    def fetchArtist(self, artist):
        debug = "";
        try:
            self.api.fetch(artist.name)
            for album_data in self.api.albums:

                album_data['artist'] = artist
                currentPrice = album_data.pop('price')
                debug = album_data
                albums = Album.objects.filter(ASIN=album_data['ASIN'], source=album_data['source'])
                if len(albums) == 0:
                    album = Album(**album_data)
                else:
                    album = albums[0]

                album.currentPrice = currentPrice
                album.lastFetched = datetime.now(pytz.utc)
                #  TODO: it seems that diferent international shops has the same albu
                if album.minPrice == 0.00 or album.minPrice > album.currentPrice:
                    album.minPrice = album.currentPrice
                    album.priceUpdated = True
                else:
                    album.priceUpdated = False
                album.save()
            artist.lastFetched = datetime.now(pytz.utc)
            artist.save()
        except Exception as e:
            print "ALERT: we couldn't fetch data from " + artist.name
            # print debug
            print e

    def updateArtistAlbums(self, artist):
        if artist.lastFetched < last_fetch_limit:
            self.fetchArtist(artist)

    def updateArtistAlbumsByName(self, name):
        artist = Artist.objects.get_or_create(name=name)[0]
        self.updateArtistAlbums(artist)

    def getArtistAlbumsByName(self, artist_name, max_price=None, filter_singles=False, currency=None):
        return self.albumsService.getExportedArtistAlbums(artist_name, max_price, filter_singles, currency)

    def getArtistAlbums(self, artist, max_price=None, filter_singles=False, currency=None):
        return self.albumsService.getExportedArtistAlbums(artist.name, max_price, filter_singles, currency)

    def getNotUpdatedArtists(self):
        artists = Artist.objects.filter(lastFetched__lte=last_fetch_limit)
        return artists

    def getArtist(self, artist_name):
        artists = Artist.objects.filter(name=artist_name)
        if len(artists) == 0:
            return None
        else:
            return artists[0]

    def createArtist(self, artist_data):
        artist = Artist(**artist_data)
        artist.save()
        self.updateArtistAlbums(artist)
        return artist




