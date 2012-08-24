from django.conf.urls.defaults import patterns, url
from commons.models import CsrfExemptResource
from user_session.handlers import User_handler, Session_handler


user_handler = CsrfExemptResource(User_handler)
session_handler = CsrfExemptResource(Session_handler)

urlpatterns = patterns('',
    url(r'^session/$', session_handler),
    url(r'^$', user_handler),
)
