import logging
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework import status

from django.contrib.auth import get_user_model

User = get_user_model()


class RequestLoggingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

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

        self.logger.info(f"{datetime.now()} - User: {user} - Path: {request.path}")

        response = self.get_response(request)
        return response


class RestrictAccessByTimeMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request, *args, **kwds):
        current_time = datetime.datetime.now().time()
        start_time = datetime.time(18, 0)  # 6:00 PM
        end_time = datetime.time(21, 0)  # 9:00 PM
        if current_time < start_time or current_time > end_time:
            return JsonResponse(
                {"detail": "You're not allowed to chat at this time"},
                status=status.HTTP_403_FORBIDDEN,
            )
        response = self.get_response(request)
        return response
