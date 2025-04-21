import logging

from django.db import models
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()


class NoteObjectManager(models.Manager):
    def create_new_note(self, user, serializer):
        try:
            return self.create(user=user, **serializer)
        except Exception as e:
            logger.error({"response": "Note object init failed", "errors": repr(e)})


class Note(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    objects = NoteObjectManager()

    def __str__(self):
        return f"{self.title}"
