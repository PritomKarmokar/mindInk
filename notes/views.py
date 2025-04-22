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
        current_user = request.user

        if serializer.is_valid():
            _ = Note.objects.create_new_note(current_user, serializer.validated_data)

            response = {
                "message": "New Note Created Successfully!",
                "data": serializer.data
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
