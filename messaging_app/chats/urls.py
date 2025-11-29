
from .views import *
from rest_framework.routers import DefaultRouter


router= DefaultRouter()

router.register(r"conversation", ConversationViewSet, basename="conversations")
router.register(r"messages", MessageViewSet, basename='messages')
