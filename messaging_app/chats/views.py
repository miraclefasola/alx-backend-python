
from django.shortcuts import render
from rest_framework import viewsets
from .models import *
from django.contrib.auth import get_user_model
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.db.models import Count


# Call the function to get the actual User model class
User = get_user_model()

class ConversationViewSet(viewsets.ModelViewSet):
    serializer_class= ConversationSerializer
    permission_classes= [IsAuthenticated]

    def get_queryset(self):
        return Conversation.objects.filter(participants=self.request.user)
    
    def create(self, request, *args, **kwargs):
        participants=request.data.get('participants', [])
        
        if len(participants) != 2:
            return Response({"detail": "A conversation requires exactly 2 participants." }, status=400)

        found_users = list(User.objects.filter(user_id__in=participants))
        if len(found_users) != 2:
            #This might look vague but the real id error would be logged by a logger, can be revealing the whole error as it might pose a risk to our app
            return Response({"detail":"one user ID is invalid"}, status=400)
        

        user_a = found_users[0]
        user_b = found_users[1]

        existing = Conversation.objects.filter(participants=user_a).filter(participants=user_b).annotate(p_count=Count('participants')).filter(p_count=2).first()

        if existing:    
            return Response({"detail": "Coversation already exists, can't duplicate"})
        else:
            serializer= self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception= True)
            conversation = serializer.save()
            conversation.participants.set([user_a, user_b])
            return Response(self.get_serializer(conversation).data, status=201)


    
class MessageViewSet(viewsets.ModelViewSet):
    serializer_class= MessageSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return Message.objects.filter(conversation__participants=self.request.user)
    
    def create(self, request, *args, **kwargs):
        #we need to grab conversation id, sender deatails
        conversation_id= self.request.data.get('conversation_id')
        sender= request.user

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
                return Response({"detail": "Invalid Conversation ID format."}, status=400)
        
        if not conversation.participants.filter(pk=sender.pk).exists():
    # If the user is not a participant, deny access (403 Forbidden)
            return Response(
                {"detail": "You are not a participant in this conversation and cannot send messages."}, 
                status=403
            )
        
        # If all checks pass, proceed with message creation
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        # Inject the validated conversation instance and the sender into the save process
        message = serializer.save(conversation=conversation, sender=sender)

        return Response(self.get_serializer(message).data, status=201)