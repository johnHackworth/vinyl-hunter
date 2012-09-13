from album.models import Album
from vendors.amazonProductApiCrawler.amazonSearch import Amazon
import re

class Album_service():

    def __init__(self):
        self.api = Amazon()


    def getArtistAlbums(self, artist_name, currency=None):
        albums = Album.objects.filter(artist=artist_name)
        if currency:
            albums = albums.filter(currency=currency)
        return albums

    def getExportedArtistAlbums(self, artist_name, max_price = None, filter_single = False, currency = None):
        albums = self.getArtistAlbums(artist_name, currency)
        exported_albums = []
        for album in albums:
            if max_price is None or float(album.currentPrice) <= float(max_price):
                if filter_single != True  or (album.format != 'Single' and album.format != 'EP'):
                    exported_albums.append(album.as_dict())
        return exported_albums

