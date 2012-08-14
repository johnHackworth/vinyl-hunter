from django.core.management.base import BaseCommand
from artist.services import Artists_service
from album.services import Album_service


class Command(BaseCommand):

    def __init__(self):
        self.album_service = Album_service()
        self.artist_service = Artists_service(self.album_service)

    def handle(self, *args, **options):

        artists = self.artist_service.getNotUpdatedArtists()
        for artist in artists:
            print artist.name
            self.artist_service.updateArtistAlbums(artist)

