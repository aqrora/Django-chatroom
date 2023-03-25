from rest_framework import serializers
from .models import Message



class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Message
        fields = ['id', 'text', 'user', 'created_at', 'updated_at']