from django.urls import path

from notes.views import NotesListCreateAPIView, NotesRetrieveUpdateDeleteAPIView

urlpatterns = [
    path("", NotesListCreateAPIView.as_view(), name="notes-create-or-list"),
    path(
        "<int:note_id>/",
        NotesRetrieveUpdateDeleteAPIView.as_view(),
        name="notes-retrieve-update-delete",
    ),
]
