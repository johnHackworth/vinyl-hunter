from django.db import models
from artist.models import Artist
from django.conf import settings

class ArtistTestCaseFactory:
    number_of_artists = 0

    def artist(self):
        artist = Artist()
        artist.name = "irrelevant name " + str(self.number_of_artists)

        artist.thumbnail = str(self.number_of_artists)
        artist.image = str(self.number_of_artists)
        artist.largeImage = str(self.number_of_artists)
        self.number_of_artists +=1
        return artist

    def persistedArtist(self):
        artist = self.artist()
        artist.save()
        return artist
