from django.conf.urls.defaults import patterns, url
from commons.models import CsrfExemptResource
from user_session.handlers import User_handler, Session_handler, User_artists_handler, User_albums_handler


user_handler = CsrfExemptResource(User_handler)
session_handler = CsrfExemptResource(Session_handler)
artist_handler = CsrfExemptResource(User_artists_handler)
albums_handler = CsrfExemptResource(User_albums_handler)

urlpatterns = patterns('',
    url(r'^session/$', session_handler),
    url(r'^(?P<identification>\w+)/artists/$', artist_handler),
    url(r'^(?P<identification>\w+)/albums/$', albums_handler),
    url(r'^artists/(?P<artist_name>[\w ]+)$', artist_handler),
    url(r'^(?P<identification>\w+)/$', user_handler),
    url(r'^$', user_handler),
)
