from rest_framework.exceptions import APIException
from rest_framework import status


class BadRequest400(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad Request'
    default_code = 'bad_request'


class NotFound404(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found'
    default_code = 'not_found'
