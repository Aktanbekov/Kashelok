from rest_framework import exceptions
from rest_framework import status


class MyException(exceptions.APIException):

    def __init__(self, status_code: int = None, detail: dict = None, code=None):
        super().__init__(detail=detail, code=code)
        if status_code is None:
            self.status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
        else:
            self.status_code = status_code
