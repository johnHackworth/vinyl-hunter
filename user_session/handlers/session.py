from django.http import HttpResponse, HttpResponseNotFound, HttpResponseForbidden, HttpResponseNotAllowed
from user_session.services import User_service, Session_service
from commons.models import ExtHandler


class Session_handler(ExtHandler):
    allowed_methods = ('POST', 'DELETE')
    user_service = User_service()
    session_service = Session_service(user_service)

    def create(self, request):

        login = request.data['login']
        password = request.data['password']
        result = self.session_service.logUser(login, password)
        if result is None:
            return HttpResponseNotFound('<h1>Incorrect login attemp</h1>')
        else:
            return HttpResponse(result)

    def delete(self, request):
        session_data = self.getSessionData(request);
        if self.session_service.validSession(session_data):
            self.session_service.deleteSession(session_data['session_id'], session_data['session_hash'])
            return HttpResponse()
        return  HttpResponseNotFound();
