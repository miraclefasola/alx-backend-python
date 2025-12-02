
import logging
from rest_framework import status
from rest_framework.response import Response
from datetime import datetime
class RequestLoggingMiddleware():
    def __init__(self, get_response):
        self.get_response=get_response

        self.logger = logging.getLogger("request_logger")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
                    fmt="%(name)s : %(asctime)s : %(levelname)s : %(pathname)s: %(funcName)s : %(message)s"
                )
        file_handler = logging.FileHandler("requests.log")
        self.logger.addHandler(file_handler)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(logging.INFO)

    def __call__(self,request, *args, **kwds):


        if not request.user.is_authenticated:
            return Response({'detail':'user must authenticated'}, status=status.HTTP_403_FORBIDDEN)
        self.logger.info (f"{datetime.now()} - User: {request.user.username} - Path: {request.path}")
        
        

        response= self.get_response(request)
        return response

