from django.core.management.base import BaseCommand
from artist.services import Artists_service
from lastFmUser.services import LastFm_user_service
from user_session.services import User_service
from settings import MAX_FETCH_BATCH
import time


class Command(BaseCommand):

    def __init__(self):
        self.artist_service = Artists_service()
        self.lastfm_service = LastFm_user_service(self.artist_service)
        self.user_service = User_service(self.lastfm_service)

    def handle(self, *args, **options):
        lastfm_users = self.lastfm_service.getNotUpdatedUsers()
        fetched_users = 0
        for lastfm_user in lastfm_users:
            if not fetched_users < MAX_FETCH_BATCH:
                break
            print "trying to fetch" + lastfm_user.name
            if self.lastfm_service.updateUser(lastfm_user):

                fetched_users = fetched_users + 1
                print "trying to update related users"
                self.user_service.refreshFromLastFmUser(lastfm_user)

        print "waiting for an hour"
        time.sleep(3600)

        self.handle()
