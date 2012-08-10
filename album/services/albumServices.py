from artist.models import Artist
from album.models import Album
from datetime import datetime
from vendors.amazonProductApiCrawler.amazonSearch import Amazon

class Album_service():

    def __init__(self):
        self.api = Amazon()


