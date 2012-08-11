class ExtException(Exception):
    txt = 'error: '
    def __init__(self, value = ""):
        self.value = value
    def __str__(self):
        return repr(self.txt+str(self.value))


class MethodNotAllowedException(ExtException):
    txt = 'Method not allowed: '


class InvalidFieldsException(ExtException):
    txt = 'Some fields are invalid: '


class InvalidPasswordException(ExtException):
    txt = 'Invalid password: '


class ExistingUserException(ExtException):
    txt = 'Invalid user: '


class ExistingEmailException(ExistingUserException):
    txt = 'Existing email: '


class ExistingLoginException(ExistingUserException):
    txt = 'Existing login: '


class TooMuchAttempsException(ExtException):
    txt = 'To much attemps '


class NotLoggedException(ExtException):
    txt = 'You need to be logged to complete this action '


class NotFoundException(ExtException):
    txt = 'The resource doesn\'t exist'
