from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed
from user_session.services import User_service, Session_service
from lastFmUser.services import LastFm_user_service
from artist.services import Artists_service
from album.services import Album_service

from commons.models import ExtHandler
from commons.exceptions import InvalidPasswordException, ExistingUserException, InvalidFieldsException

class User_handler(ExtHandler):

    allowed_methods = ('OPTIONS, GET, POST, PUT, DELETE')
    lastFm_service = LastFm_user_service(Artists_service(Album_service()))
    user_service = User_service(lastFm_service)
    session_service = Session_service(user_service)
    fields = ["name", "lastname", "email", "location", "country", "gender", "about", "language"]
    update_fields = ["name", "lastname", "location", "country", "gender", "about", "language"]

    def getUser(self, value, field):
        user = self.user_service.findUser({field: value})
        if user is not None:
            return HttpResponse(user.as_json())
        else:
            return HttpResponseNotFound('<h1>User not found</h1>')

    def read(self, request, identification):
        if identification.isdigit():
            return self.getUser(identification, "id")
        else:
            return self.getUser(identification, "login")

    def update(self, request):
        sessionDTO = self.getSessionData(request)
        loggedUser = self.session_service.getLoggedUser(sessionDTO)
        if loggedUser is not None:
            if 'lastFmUser' not in request.data:
                return self.updateUserData(request, loggedUser)
            else:
                return self.updateLastFmUser(request, loggedUser)
        else:
            return HttpResponseForbidden('<h1>not a user</h1>')


    def updateUserData(self, request, loggedUser):
        self.fromRequest(request, loggedUser, self.update_fields)
        try:
            loggedUser = self.user_service.saveUser(loggedUser, True)
        except InvalidFieldsException as invalid_fields:
            return HttpResponseForbidden(invalid_fields)
        except ExistingUserException as invalid_user:
            return HttpResponseForbidden(invalid_user)
        return HttpResponse(loggedUser.as_json())

    def updateLastFmUser(self, request, loggedUser):
        self.user_service.searchAndAssignLastFmUser (loggedUser, request.data['lastFmUser'])
        return self.user_service.getUserArtists(loggedUser)


    def create(self, request):
        user = self.user_service.createUser()
        self.fromRequest(request, user, self.fields)

        user.login = request.data['login']
        if not 'password' in request.data:
            return HttpResponseForbidden('Password required')

        try:
            self.user_service.assignPassword(user, None, request.data['password'])
        except InvalidPasswordException as invalid_password:
            return HttpResponseForbidden(str(invalid_password))
        try:
            user = self.user_service.saveUser(user)
        except InvalidFieldsException as invalid_fields:
            return HttpResponseForbidden(invalid_fields)
        except ExistingUserException as invalid_user:
            return HttpResponseForbidden(invalid_user)

        return HttpResponse(user.as_json())

