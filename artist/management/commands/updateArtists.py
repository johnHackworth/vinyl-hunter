from django.core.management.base import BaseCommand
from artist.services import Artists_service
from album.services import Album_service
from settings import MAX_FETCH_BATCH
import time

class Command(BaseCommand):

    def __init__(self):
        self.album_service = Album_service()
        self.artist_service = Artists_service(self.album_service)

    def handle(self, *args, **options):
        artists = self.artist_service.getNotUpdatedArtists()
        fetched_artists = 0
        for artist in artists:
            if not fetched_artists < MAX_FETCH_BATCH:
                break;
            print 'fetching ' + artist.name
            self.artist_service.updateArtistAlbums(artist)
            fetched_artists = fetched_artists +1

        print "waiting for an ten minutes"
        time.sleep(600)

        self.handle()
