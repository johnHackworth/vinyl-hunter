from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed
from user_session.services import User_service, Session_service
from commons.models import ExtHandler


class Session_handler(ExtHandler):
    allowed_methods = ('POST')
    user_service = User_service()
    session_service = Session_service(user_service)

    def create(self, request):

        login = request.POST.get('username')
        password = request.POST.get('password')
        result = self.session_service.logUser(login, password)
        if result is None:
            return HttpResponseNotFound('<h1>Incorrect login attemp</h1>')
        else:
            return HttpResponse(result)
