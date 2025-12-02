import logging
from datetime import datetime
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.http import JsonResponse
from rest_framework import status
import time

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


from django.core.cache import cache

BANNED_WORDS = ["fuckyou", "pussy","kill" ,"suicide"]
MAX_MESSAGES_PER_MINUTE = 5

class OffensiveLanguageMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        if request.method == "POST":
            ip = request.META.get("REMOTE_ADDR", "unknown")

            # --- Rate Limiting ---
            cache_key = f"msg_count_{ip}"
            count = cache.get(cache_key, 0)

            if count >= MAX_MESSAGES_PER_MINUTE:
                return JsonResponse({"detail": "Too many messages, try again later"}, status=429)

            cache.set(cache_key, count + 1, timeout=60)  # expires in 60 seconds

            message_body = request.data.get("message_body", "") if hasattr(request, "data") else ""
            if any(bad_word in message_body.lower() for bad_word in BANNED_WORDS):
                return JsonResponse({"detail": "Offensive language is not allowed"}, status=400)



        response = self.get_response(request)
        return response


# chats/middleware.py


import re

class RolepermissionMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        # List of regex patterns for protected endpoints
        self.protected_patterns = [
            r"^/api/messages/\d+/$",                        # message delete or detail
            r"^/api/conversations/\d+/messages/\d+/$",     # nested message delete
            r"^/api/conversations/\d+/$",                  # conversation delete
        ]

    def __call__(self, request, *args, **kwargs):
        path = request.path

        # Only enforce role check for protected patterns
        for pattern in self.protected_patterns:
            if re.match(pattern, path):
                # Check authentication
                if not request.user.is_authenticated:
                    return JsonResponse(
                        {"detail": "Authentication required"},
                        status=status.HTTP_403_FORBIDDEN
                    )

                # Check role
                if request.user.role not in ["admin", "moderator"]:
                    return JsonResponse(
                        {"detail": "You do not have permission to perform this action"},
                        status=status.HTTP_403_FORBIDDEN
                    )
                break  # Stop checking other patterns

        response = self.get_response(request)
        return response
