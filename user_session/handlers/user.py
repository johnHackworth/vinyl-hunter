from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed
from user_session.services import User_service, Session_service
from commons.models import ExtHandler
from commons.exceptions import InvalidPasswordException, ExistingUserException, InvalidFieldsException

class User_handler(ExtHandler):

    allowed_methods = ('GET, POST, PUT, DELETE')
    user_service = User_service()
    session_service = Session_service(user_service)
    fields = ["name", "lastname", "email", "location", "country", "gender", "aboutme", "languaje"]

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
            self.fromRequest(request, loggedUser, self.fields)
            try:
                loggedUser = self.user_service.saveUser(loggedUser)
            except InvalidFieldsException as invalid_fields:
                return HttpResponseForbidden(invalid_fields)
            except ExistingUserException as invalid_user:
                return HttpResponseForbidden(invalid_user)
            return HttpResponse(loggedUser.as_json())
        else:
            return HttpResponseForbidden('<h1>not a user</h1>')

    def create(self, request):
        user = self.user_service.createUser()
        self.fromRequest(request, user, self.fields)

        user.login = request.POST.get('login')
        try:

            self.user_service.assignPassword(user, None, request.POST.get('password'))
        except InvalidPasswordException as invalid_password:
            return HttpResponseForbidden(str(invalid_password))
        try:
            user = self.user_service.saveUser(user)
        except InvalidFieldsException as invalid_fields:
            return HttpResponseForbidden(invalid_fields)
        except ExistingUserException as invalid_user:
            return HttpResponseForbidden(invalid_user)

        return HttpResponse(user.as_json())

