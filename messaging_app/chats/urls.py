from django.contrib import admin
from django.urls import path, include
from .views import *
from rest_framework import routers as drf_routers
from rest_framework_nested import routers as nested_routers



router= drf_routers.DefaultRouter()

router.register(r"conversations", ConversationViewSet, basename="conversations")
router.register(r"messages", MessageViewSet, basename="messages")

conversation_router=nested_routers.NestedDefaultRouter(router, r"conversations", "conversation")

conversation_router.register(r"messages", MessageViewSet, basename="conversation_messages")

urlpatterns = [
    path("", include(router.urls)),
    path("", include(conversation_router.urls))
]
