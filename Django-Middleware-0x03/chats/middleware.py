
import logging
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication

from django.contrib.auth import get_user_model

User= get_user_model()

class RequestLoggingMiddleware():
    def __init__(self, get_response):
        self.get_response=get_response

        self.logger = logging.getLogger("request_logger")
        self.logger.setLevel(logging.INFO)
        formatter = logging.Formatter(
                    fmt="%(name)s : %(asctime)s : %(levelname)s : %(pathname)s: %(funcName)s : %(message)s"
                )
        file_handler = logging.FileHandler("requests.log")
        file_handler.setFormatter(formatter)
        self.logger.addHandler(file_handler)
        
        file_handler.setLevel(logging.INFO)

    def __call__(self, request, *args, **kwds):

        try:
            user_auth = JWTAuthentication()
            auth_result = user_auth.authenticate(request)
            if auth_result is not None:
                request.user = auth_result[0]
        except Exception:
            pass

        
        if not request.user.is_authenticated:
            user = "Guest"
        else:
            user = request.user.username

        self.logger.info (f"{datetime.now()} - User: {user} - Path: {request.path}")
        
        

        response= self.get_response(request)
        return response

