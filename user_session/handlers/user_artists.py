from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseBadRequest
from lastFmUser.services import LastFm_user_service
from artist.services import Artists_service
from user_session.services import User_service, Session_service
from commons.models import ExtHandler


class User_artists_handler(ExtHandler):
    allowed_methods = ('GET', 'PUT', 'DELETE')
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
            response = self.user_service.getExportedArtists(user)
            return HttpResponse(response)

    def update(self, request, artist_name = None):
        if artist_name is None:
            return HttpResponseBadRequest()
        sessionDTO = self.getSessionData(request)
        loggedUser = self.session_service.getLoggedUser(sessionDTO)
        if loggedUser is not None:
            self.user_service.addArtist(loggedUser, artist_name)
            response = self.user_service.getExportedArtists(loggedUser)
            return HttpResponse(response)
        else:
            return HttpResponseForbidden()

    def delete(self, request, artist_name = None):
        if artist_name is None:
            return HttpResponseBadRequest()
        sessionDTO = self.getSessionData(request)
        loggedUser = self.session_service.getLoggedUser(sessionDTO)
        if loggedUser is not None:
            artists_name = artist_name
            self.user_service.ignoreArtist(loggedUser, artist_name)
            response = self.user_service.getExportedArtists(loggedUser)
            return HttpResponse(response)
        else:
            return HttpResponseForbidden()
