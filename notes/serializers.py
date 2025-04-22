from rest_framework import serializers


class NoteSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=50)
    content = serializers.CharField(max_length=1000)
