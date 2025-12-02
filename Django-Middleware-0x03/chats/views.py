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
            return Response({"detail": "Other participant username is required."}, status=400)

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
    filterset_class= MessageFilter
    ordering_fields = []
    ordering = []
    pagination_class = MessagePagination

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)

    def create(self, request, *args, **kwargs):
        # we need to grab conversation id, sender deatails
        conversation_id = self.request.data.get("conversation_id")
        sender = request.user

        """Now we need our error handdling on point
        1. We need to make sure conversation_ID is valid
        2. Confirm sender is active in DB
        3. Confirm the sender has established a conversation and therefore has rigts to send mesages and attach to a conversation
        """
        if conversation_id:
            try:
                # Attempt to retrieve the conversation instance by ID
                conversation = Conversation.objects.get(conversation_id=conversation_id)
            except Conversation.DoesNotExist:
                # If not found, return a 404 (Not Found)
                return Response({"detail": "Conversation not found."}, status=404)
            except serializer.ValidationError:
                # Handles cases where conversation_id is not a valid UUID format
                return Response(
                    {"detail": "Invalid Conversation ID format."}, status=400
                )

        if not conversation.participants.filter(pk=sender.pk).exists():
            # If the user is not a participant, deny access (403 Forbidden)
            return Response(
                {
                    "detail": "You are not a participant in this conversation and cannot send messages."
                },
                status=status.HTTP_403_FORBIDDEN,
            )

        # If all checks pass, proceed with message creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Inject the validated conversation instance and the sender into the save process
        message = serializer.save(conversation=conversation, sender=sender)

        return Response(self.get_serializer(message).data, status=201)
