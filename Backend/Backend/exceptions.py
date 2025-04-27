from rest_framework.exceptions import APIException
from rest_framework.views import exception_handler
from rest_framework import status


class BadRequest400(APIException):
    status_code = status.HTTP_400_BAD_REQUEST
    default_detail = 'Bad Request'
    default_code = 'bad_request'

    # def __init__(self, detail=None, code=None):
    #     self.code = code
    #     super().__init__(detail, code)

    # def get_full_details(self):
    #     return {
    #         'code': self.code,
    #         'detail': self.detail,
    #     }


class NotFound404(APIException):
    status_code = status.HTTP_404_NOT_FOUND
    default_detail = 'Not found'
    default_code = 'not_found'


def custom_exception_handler(exc, context):
    """
        Add code for APIException to response
    """
    response = exception_handler(exc, context)
    
    if response is not None and hasattr(exc, 'get_codes'):
        response.data['code'] = exc.get_codes()
        # For APIException with a single code:
        if hasattr(exc, 'code'):
            response.data['code'] = exc.code
    
    return response
