from rest_framework import serializers
from .models import *
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError

# Call the function to get the actual User model class
User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    full_name= serializers.SerializerMethodField()
    class Meta:
        model= User
        fields=["user_id", "username","full_name","first_name", "last_name", "email", "phone_number", "created_at", "role" ]

    def get_full_name(self, obj):
        return f" {obj.first_name} {obj.last_name}"

class MessageSerializer(serializers.ModelSerializer):
    
    sender=serializers.StringRelatedField(read_only=True)
    conversation_id= serializers.UUIDField(source="conversation.conversation_id", read_only=True)
    class Meta:
        model= Message
        fields=["message_id", "sender","conversation_id", "message_body", "sent_at" ]

class ConversationSerializer(serializers.ModelSerializer):
    participants= UserSerializer(many=True, read_only=True)
    messages=MessageSerializer(many=True, read_only=True )
    
    class Meta:
        model= Conversation
        fields=["conversation_id","messages" ,"participants", "created_at", "updated_at"]

    def validate(self, attrs):
        participants= attrs.get('participants', [])
        if len(participants) < 2:
            raise serializers.ValidationError('A coversation should involve two Participants')
        return attrs