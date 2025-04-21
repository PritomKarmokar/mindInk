from django.urls import path

from notes.views import NotesListCreateAPIView

urlpatterns = [
    path("", NotesListCreateAPIView.as_view(), name="notes-create-or-list"),
]
