from django.conf.urls.defaults import patterns, url
from commons.models import CsrfExemptResource
from artist.handlers import Artist_albums_handler


albums_handler = CsrfExemptResource(Artist_albums_handler)

urlpatterns = patterns('',
    url(r'^(?P<artist_name>[\w\-\ ]+)/albums/$', albums_handler),
)
