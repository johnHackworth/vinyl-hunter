from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from lastFmUser.services import LastFm_user_service
from artist.services import Artists_service
from user_session.services import User_service, Session_service
from commons.models import ExtHandler


class User_albums_handler(ExtHandler):
    allowed_methods = ('GET')
    lastFm_service = LastFm_user_service(Artists_service())
    user_service = User_service(lastFm_service)
    session_service = Session_service(user_service)

    def read(self, request, identification = None):
        if identification is None:
            return HttpResponseBadRequest()
        user = self.user_service.findUser(id=identification)
        if user is None:
            return HttpResponseNotFound()
        else:
            if "maxPrice" in request.GET:
                max_price = request.GET["maxPrice"]
            else:
                max_price = None

            user = self.lastfm_service.fetchAll(username)
            response = self.lastfm_service.getUserAlbums(user, max_price)
            return HttpResponse(response)

