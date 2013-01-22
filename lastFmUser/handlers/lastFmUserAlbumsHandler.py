from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed
from artist.services import Artists_service
from lastFmUser.services import LastFm_user_service
from album.services import Album_service
from commons.models import ExtHandler


class LastFm_user_albums_handler(ExtHandler):
    allowed_methods = ('GET, PUT, POST')

    def __init__(self):
        self.album_service = Album_service()
        self.artist_service = Artists_service(self.album_service)
        self.lastfm_service = LastFm_user_service(self.artist_service)

    def create(self, request, username):
        pass

    def update(self, request, username):
        pass

    def read(self, request, username):
        if "maxPrice" in request.GET:
            max_price = request.GET["maxPrice"]
        else:
            max_price = None

        if "excludeSingles" in request.GET:
            exclude_singles = ((request.GET["excludeSingles"] == 'True') or (request.GET["excludeSingles"] == 'true'))
        else:
            exclude_singles = False

        if "currency" in request.GET:
            currency = request.GET["currency"]
        else:
            currency = False

        user = self.lastfm_service.fetchAll(username)
        response = self.lastfm_service.getUserAlbums(user, max_price, exclude_singles, currency)
        return response

