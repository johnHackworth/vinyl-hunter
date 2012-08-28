from django.test import TestCase
from album.models import *
from album.services import *
from album.mocks import  AlbumsTestCaseFactory
from django.utils.unittest import skipIf
from django.conf import settings
from crypt import crypt
from datetime import timedelta

import json


class AlbumServiceTest(TestCase):
    cases_factory = AlbumsTestCaseFactory()
    album_service = Album_service()

    def test_getArtistAlbums(self):
        album1 = self.cases_factory.persistedAlbum()
        album2 = self.cases_factory.persistedAlbum()

        albums = self.album_service.getArtistAlbums(self.cases_factory.artist.name)

        self.assertEqual(len(albums), 2)
        self.assertEqual(albums[0].ASIN, album1.ASIN)
        self.assertEqual(albums[1].ASIN, album2.ASIN)

    def test_getExportedArtistAlbums(self):
        self.cases_factory.newArtist()

        album1 = self.cases_factory.persistedAlbum()
        album1.currentPrice = 2000
        album1.save()
        album2 = self.cases_factory.persistedAlbum()
        album2.format = 'EP'
        album2.save()

        # no limitations
        albums = self.album_service.getExportedArtistAlbums(self.cases_factory.artist.name)
        self.assertEqual(len(albums), 2)
        self.assertEqual(albums[0]['ASIN'], album1.ASIN)
        self.assertEqual(albums[1]['ASIN'], album2.ASIN)

        # price limit
        albums = self.album_service.getExportedArtistAlbums(self.cases_factory.artist.name, 1000)
        self.assertEqual(len(albums), 1)
        self.assertEqual(albums[0]['ASIN'], album2.ASIN)

        # format limit
        albums = self.album_service.getExportedArtistAlbums(self.cases_factory.artist.name, None, True)
        self.assertEqual(len(albums), 1)
        self.assertEqual(albums[0]['ASIN'], album1.ASIN)

