from album.models import Album
from vendors.amazonProductApiCrawler.amazonSearch import Amazon


class Album_service():

    def __init__(self):
        self.api = Amazon()

    def getArtistAlbums(self, artist_name):
        albums = Album.objects.filter(artist=artist_name)
        return albums

    def getExportedArtistAlbums(self, artist_name, max_price = None):
        albums = self.getArtistAlbums(artist_name)
        exported_albums = []
        for album in albums:
            if max_price is None or float(album.currentPrice) <= float(max_price):
                exported_albums.append(album.as_dict())
        return exported_albums

