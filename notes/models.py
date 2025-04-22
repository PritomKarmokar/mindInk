import logging
import typing

from typing import Any, Dict

from django.db import models
from django.contrib.auth import get_user_model

logger = logging.getLogger(__name__)

User = get_user_model()


class NoteObjectManager(models.Manager):
    def create_new_note(
        self, user: User, validated_data: dict
    ) -> typing.Optional["Note"]:
        try:
            return self.create(user=user, **validated_data)
        except Exception as e:
            logger.error(
                {"response": "Note object init failed", "errors": repr(e)},
                exc_info=True,
            )
            raise Exception("Note object init failed")


class Note(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    objects = NoteObjectManager()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Notes"
        verbose_name_plural = "Notes List"
        db_table = "notes"
