from django.conf.urls.defaults import patterns, url
from commons.models import CsrfExemptResource
from lastFmUser.handlers import LastFm_user_handler, LastFm_user_albums_handler


lastFm_user_handler = CsrfExemptResource(LastFm_user_handler)
lastFm_user_albums_handler = CsrfExemptResource(LastFm_user_albums_handler)

urlpatterns = patterns('',
    url(r'^artists/(?P<username>\w+)/$', lastFm_user_handler),
    url(r'^albums/(?P<username>\w+)/$', lastFm_user_albums_handler),
)
