from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers


router= routers.DefaultRouter()

router.register(r"conversation", ConversationViewSet, basename="conversations")
router.register(r"messages", MessageViewSet, basename='messages')
