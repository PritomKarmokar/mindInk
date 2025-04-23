from django.utils import timezone

from rest_framework import status
from rest_framework.views import APIView
from rest_framework.request import Request
from rest_framework.response import Response

from notes.models import Note
from notes.serializers import NoteSerializer


class NotesListCreateAPIView(APIView):
    serializer_class = NoteSerializer

    def get(self, request: Request) -> Response:
        notes_list = Note.objects.get_note_object_list(user=request.user)
        if notes_list:
            serializer = self.serializer_class(instance=notes_list, many=True)
            response = {
                "message": f"Currently Available Notes for {request.user.username}",
                "notes": serializer.data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": f"{request.user}, Currently you have no notes",
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

    def post(self, request: Request) -> Response:
        serializer = self.serializer_class(data=request.data)
        current_user = request.user

        if serializer.is_valid():
            _ = Note.objects.create_new_note(current_user, serializer.validated_data)

            response = {
                "message": "New Note Created Successfully!",
                "data": serializer.data,
            }
            return Response(data=response, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class NotesRetrieveUpdateDeleteAPIView(APIView):
    serializer_class = NoteSerializer

    def get(self, request: Request, note_id: int) -> Response:
        note = Note.objects.get_note_object(note_id=note_id)
        if note:
            serializer = self.serializer_class(note)
            response = {
                "message": f"Note with the ID {note_id} was Retrieved Successfully!",
                "data": serializer.data,
            }
            return Response(data=response, status=status.HTTP_200_OK)
        else:
            response = {
                "message": f"Note with the ID {note_id} does not exist",
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request: Request, note_id: int) -> Response:
        title = request.data.get("title", None)
        content = request.data.get("content", None)

        note = Note.objects.get_note_object(note_id=note_id)

        if not note:
            response = {
                "message": f"Note with the ID {note_id} does not exist",
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        if not title and not content:
            error_response = {
                "message": "title or content is required. both values cannot be None"
            }
            return Response(data=error_response, status=status.HTTP_400_BAD_REQUEST)
        else:
            _ = note.update_object(title=title, content=content)
            response = {
                "message": f"Note with the ID {note_id} Updated Successfully!",
            }
            return Response(data=response, status=status.HTTP_200_OK)

    def delete(self, request: Request, note_id: int) -> Response:
        note = Note.objects.get_note_object(note_id=note_id)
        if not note:
            response = {
                "message": f"Note with the ID {note_id} does not exist",
            }
            return Response(data=response, status=status.HTTP_404_NOT_FOUND)

        note.delete_object()

        response = {
            "message": f"Note with the ID {note_id} Deleted Successfully!",
        }
        return Response(data=response, status=status.HTTP_204_NO_CONTENT)
