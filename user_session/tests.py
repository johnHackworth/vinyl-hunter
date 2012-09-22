from django.test import TestCase
from user_session.models import *
from user_session.services import *
from user_session.mocks import UsersTestCaseFactory
from django.utils.unittest import skipIf
from django.conf import settings
from crypt import crypt
from commons.exceptions import InvalidFieldsException, InvalidPasswordException, TooMuchAttempsException
from datetime import timedelta

import json


class UserModelTest(TestCase):
    casesFactory = UsersTestCaseFactory()

    def test_export_dictionary(self):
        user = self.casesFactory.user()

        dictObj = user.as_dict(['name', 'lastname', 'country'])
        self.assertEqual(dictObj['name'], 'Johnathan Percival')
        self.assertEqual(dictObj['lastname'], 'Hackworth')
        self.assertEqual(dictObj['country'], 1)
        try:
            gender = dictObj['gender']
            self.assertFalse(True)
        except:
            self.assertTrue(True)

        dictObj = user.as_dict(['gender'])
        try:
            country = dictObj['country']
            self.assertFalse(True)
        except:
            self.assertTrue(True)
        self.assertTrue(dictObj['gender'] == 1)

    def test_export_json(self):
        user = self.casesFactory.user()
        jsonObj = user.as_json(['name'])
        self.assertTrue(jsonObj =='{"name": "Johnathan Percival"}')

    def test_validate(self):
        user = self.casesFactory.user()
        user.login = None
        user.password = None
        user.email = None
        try:
            user.validate()
            self.fail()
        except InvalidFieldsException:
            self.assertTrue(True)
        except:
            self.fail('bad type of exception (1)')

        user.login = 'abcdef'
        try:
            user.validate()
            self.fail()
        except InvalidFieldsException:
            self.assertTrue(True)
        except:
            self.fail('bad type of exception (2)')

        user.password = 'abcdef '
        try:
            user.validate()
            self.fail()
        except InvalidFieldsException:
            self.assertTrue(True)
        except:
            self.fail('bad type of exception (3)')

        user.email = 'javi@javi.es'
        try:
            user.validate()
        except:
            self.fail()

class sessionServiceTest(TestCase):
    casesFactory = UsersTestCaseFactory()
    user_service = User_service()
    session_service = Session_service(user_service)

    def test_create_session(self):
        user = self.casesFactory.persistedUser()

        session = self.session_service.createSession(user.id)
        self.assertTrue(session.user.id == user.id)
        self.assertTrue(session.hash is not None)
        self.assertTrue(len(session.hash) > 10)

    def test_delete_session(self):
        user = self.casesFactory.user()
        user.save()
        session = self.session_service.createSession(user.id)
        session.save()
        self.session_service.deleteSession(session.id, session.hash)
        userSession = self.session_service.getSession(user.id, session.id, session.hash)

        self.assertTrue(userSession is None)

    def test_getSession(self):
        user = self.casesFactory.user()
        user.save()
        session = self.session_service.createSession(user.id)
        session.save()
        userSession = self.session_service.getSession(user.id, session.id, session.hash)
        self.assertFalse(userSession is None)
        self.assertTrue(userSession.id == session.id)
        self.assertTrue(userSession.user == user)

    def test_logUser(self):
        user = self.casesFactory.user()
        user.save()
        session = self.session_service.logUser('theAlchemist', 'abcde')
        self.assertFalse(session == None)

    def test_getLoggedUser(self):
        user = self.casesFactory.user()
        user.save()
        session = self.session_service.createSession(user.id)
        session.save()
        sessionDTO = {"session_id": session.id, "user_id": user.id, "session_hash": session.hash}
        loggedUser = self.session_service.getLoggedUser(sessionDTO)

        self.assertFalse(loggedUser is None)
        self.assertEquals(user.id, loggedUser.id)



class userServiceTest(TestCase):
    casesFactory = UsersTestCaseFactory()
    user_service = User_service()
    session_service = Session_service(user_service)

    def test_findUser(self):
        newUsers = self.casesFactory.users()

        user1 = self.user_service.findUser(name="Orolo")

        self.assertEquals(user1.name, "Orolo")
        self.assertEquals(user1.login, "orolo")

        user2 = self.user_service.findUser(login="erasmas")
        self.assertEquals(user2.name, "Erasmas")
        self.assertEquals(user2.login, "erasmas")

        user3 = self.user_service.findUser(login="Fra")
        self.assertEquals(user3, None)


    def test_saveUser(self):
        user = User()
        try:
            self.user_service.saveUser(user)
            self.fail()
        except InvalidFieldsException:
            self.assertTrue(True)

        user.login = 'prueba'
        user.password = 'prueba'
        user.email = 'prueba@prueba.es'

        try:
            user = self.user_service.saveUser(user)
        except:
            self.fail()

        userDB = self.user_service.findUser(login="prueba")

        self.assertEquals(user.id, userDB.id)

    def test_saveRepeatedUser(self):

        user = User()
        user.login = 'prueba'
        user.password = 'prueba'
        user.email = 'prueba@prueba.es'
        try:
            self.user_service.saveUser(user)
        except:
            self.fail()

        user2 = User()
        user2.login = 'prueba'
        user2.password = 'prueba'
        user2.email = 'prueba2@prueba.es'
        success = False
        try:
            self.user_service.saveUser(user2)
        except:
            success = True
        self.assertTrue(success)

        user3 = User()
        user3.login = 'prueba3'
        user3.password = 'prueba'
        user3.email = 'prueba@prueba.erasmas'
        success = False
        try:
            self.user_service.saveUser(user3)
        except:
            success = True
        self.assertTrue(success)

    def test_userSessionInfo(self):
        newUsers = self.casesFactory.users()
        user1 = self.user_service.findUser({"name" : "Orolo"})
        session = self.session_service.createSession(user1.id)

        userSessionInfo = self.user_service.userSessionInfo(user1, session)

        testCase = user1.as_dict()
        testCase2 = session.as_dict(["id", "hash"])
        testCase["session"] = testCase2
        testCase = json.dumps(testCase)

        self.assertEquals(testCase, userSessionInfo)

    def test_assignPassword(self):

        newUsers = self.casesFactory.users()
        user1 = self.user_service.findUser({"name" : "Orolo"})

        success = False
        try:
            self.user_service.assignPassword(user1, 'prueba', 'prueba2')
        except InvalidPasswordException:
            success = True
        except:
            success = False
        self.assertTrue(success)

        try:
            self.user_service.assignPassword(user1, 'abcde', 'prueba2')
            success = True
        except:
            success = False

        self.assertTrue(success)

    def test_assignNonePassword(self):
        newUsers = self.casesFactory.users()
        user1 = self.user_service.findUser({"name" : "Orolo"})

        success = False

        try:
            self.user_service.assignPassword(user1, 'prueba2', 'prueba2')
        except InvalidPasswordException:
            success = True
        except:
            success = False
        self.assertTrue(success)

