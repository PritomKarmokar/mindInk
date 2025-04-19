from rest_framework import serializers

from notes.models import Note


class NoteSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=30)
    content = serializers.CharField(max_length=1000)
