from django.shortcuts import render
from rest_framework import viewsets, status
from .models import *
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count
from rest_framework import filters
from .permissions import IsParticipantOfConversation
from chats.pagination import MessagePagination
from chats.filters import MessageFilter

# Call the function to get the actual User model class
User = get_user_model()


class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class = ConversationSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = MessagePagination

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)

    def create(self, request, *args, **kwargs):
        # Collect the other participant's username from the request
        other_username = request.data.get("participant")
        if not other_username:
            return Response(
                {"detail": "Other participant username is required."}, status=400
            )

        try:
            other_user = User.objects.get(username=other_username)
        except User.DoesNotExist:
            return Response({"detail": "User does not exist."}, status=404)

        # Check if a conversation between these two users already exists
        existing = (
            Conversation.objects.filter(participants=request.user)
            .filter(participants=other_user)
            .annotate(p_count=Count("participants"))
            .filter(p_count=2)
            .first()
        )
        if existing:
            return Response({"detail": "Conversation already exists."}, status=400)

        # Create conversation and set participants
        conversation = Conversation.objects.create()
        conversation.participants.set([request.user, other_user])

        serializer = self.get_serializer(conversation)
        return Response(serializer.data, status=201)


class MessageViewSet(viewsets.ModelViewSet):
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated, IsParticipantOfConversation]
    filter_backends = [filters.SearchFilter, filters.OrderingFilter]
    search_fields = ["sender__username", "sent_at", "conversation__conversation_id"]
    filterset_class = MessageFilter
    ordering_fields = []
    ordering = []
    pagination_class = MessagePagination

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)


def create(self, request, *args, **kwargs):
    # 1. Get conversation_id from either body or URL kwargs
    conversation_id = request.data.get("conversation_id") or self.kwargs.get(
        "conversation_id"
    )
    if not conversation_id:
        return Response({"detail": "conversation_id is required."}, status=400)

    sender = request.user

    # 2. Validate the conversation_id and fetch the conversation object
    try:
        conversation = Conversation.objects.get(conversation_id=conversation_id)
    except Conversation.DoesNotExist:
        return Response({"detail": "Conversation not found."}, status=404)
    except Exception:
        return Response({"detail": "Invalid Conversation ID format."}, status=400)

    # 3. Check if sender belongs to this conversation
    if not conversation.participants.filter(id=sender.id).exists():
        return Response(
            {"detail": "You are not a participant in this conversation."}, status=403
        )

    # 4. Validate message body
    serializer = self.get_serializer(data=request.data)
    serializer.is_valid(raise_exception=True)

    # 5. Save with injected conversation + sender
    message = serializer.save(conversation=conversation, sender=sender)

    return Response(self.get_serializer(message).data, status=201)
