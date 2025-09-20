from rest_framework.views import exception_handler
from rest_framework.response import Response
from rest_framework import status


def custom_exception_handler(exc, context):
    response = exception_handler(exc, context)
    
    if response is not None:
        custom_response_data = {
            'error': True,
            'message': 'An error occurred',
            'details': response.data
        }
        
        if hasattr(exc, 'detail'):
            if isinstance(exc.detail, dict):
                custom_response_data['message'] = 'Validation failed'
            else:
                custom_response_data['message'] = str(exc.detail)
        
        response.data = custom_response_data
    
    return response


class ValidationError(Exception):
    def __init__(self, message, field=None):
        self.message = message
        self.field = field
        super().__init__(self.message)