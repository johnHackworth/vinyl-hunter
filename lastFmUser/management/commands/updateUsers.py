from django.core.management.base import BaseCommand
from artist.services import Artists_service
from lastFmUser.services import LastFm_user_service
from settings import MAX_FETCH_BATCH


class Command(BaseCommand):

    def __init__(self):
        self.artist_service = Artists_service()
        self.lastfm_service = LastFm_user_service(self.artist_service)

    def handle(self, *args, **options):
        users = self.lastfm_service.getNotUpdatedUsers()
        fetched_users = 0
        for user in users:
            if not fetched_users < MAX_FETCH_BATCH:
                break
            print user.name
            self.lastfm_service.updateUser(user)
