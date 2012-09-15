from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed
from artist.services import Artists_service
from lastFmUser.services import LastFm_user_service
from commons.models import ExtHandler


class LastFm_user_handler(ExtHandler):
    allowed_methods = ('GET, PUT, POST')

    def __init__(self):
        self.artist_service = Artists_service()
        self.lastfm_service = LastFm_user_service(self.artist_service)

    def create(self, request, username):
        pass

    def update(self, request, username):
        pass

    def read(self, request, username):
        user = self.lastfm_service.updateUserByName(username)
        response = self.lastfm_service.getExportedArtists(user)
        return response

