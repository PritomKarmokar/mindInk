from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from notes.models import Note
from notes.serializers import NoteSerializer


class NotesListCreateAPIView(APIView):
    serializer_class = NoteSerializer

    def get(self, request: Request) -> Response:
        return Response({})

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        user = request.user
        print(user)

        if serializer.is_valid():
            new_note = Note.objects.create_new_note(user, serializer.validated_data)
            response = {
                "note": new_note
            }  # todo: throws error that `note data` is not json serializable
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
