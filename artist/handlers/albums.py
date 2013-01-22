from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from lastFmUser.services import LastFm_user_service
from artist.services import Artists_service
from album.services import Album_service
from user_session.services import User_service, Session_service
from commons.models import ExtHandler


class Artist_albums_handler(ExtHandler):
    allowed_methods = ('GET')
    artist_service = Artists_service(Album_service())
    lastFm_service = LastFm_user_service(artist_service)
    user_service = User_service(lastFm_service)
    session_service = Session_service(user_service)

    def read(self, request, artist_name = None):
        if artist_name is None:
            return HttpResponseBadRequest()
        artist = self.artist_service.findArtist(artist_name)
        if artist is None:
            # TODO: if the artists is not found try to fecth it from lastfm
            return HttpResponseNotFound()
        else:
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
            #TODO: give album status (ignored, bought, etc) if a user is logged
            response = self.artist_service.getArtistAlbums(artist, max_price, exclude_singles, currency)
            return HttpResponse(response)

