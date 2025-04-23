from django.urls import path

from notes.views import (
    NoteHomeAPIView,
    NotesListCreateAPIView,
    NotesRetrieveUpdateDeleteAPIView,
)

urlpatterns = [
    path("home/", NoteHomeAPIView.as_view(), name="home"),
    path("", NotesListCreateAPIView.as_view(), name="notes-create-or-list"),
    path(
        "<int:note_id>/",
        NotesRetrieveUpdateDeleteAPIView.as_view(),
        name="notes-retrieve-update-delete",
    ),
]
