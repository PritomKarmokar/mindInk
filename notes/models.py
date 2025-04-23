import logging
import typing

from django.db import models
from django.contrib.auth import get_user_model
from django.db.models import QuerySet
from django.utils import timezone

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
            return None

    def get_note_object(self, note_id: int) -> typing.Optional["Note"]:
        try:
            return self.get(id=note_id, is_active=True)
        except Exception as e:
            logger.error(
                {"response": "Note object fetch failed", "errors": repr(e)},
            )
            return None

    def get_note_object_list(self, user: User) -> typing.Optional[QuerySet]:
        try:
            return self.filter(user=user, is_active=True)
        except Exception as e:
            logger.error("Note list fetch failed. Errors: ", repr(e))
            return None


class Note(models.Model):
    title = models.CharField(max_length=50)
    content = models.TextField()
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notes")

    objects = NoteObjectManager()

    def __str__(self):
        return f"{self.title}"

    class Meta:
        verbose_name = "Notes"
        verbose_name_plural = "Notes List"
        db_table = "notes"

    def update_object(self, title: str, content: str) -> bool:
        try:
            if title:
                self.title = title

            if content:
                self.content = content

            self.updated_at = timezone.now()
            self.save()
            return True
        except Exception as e:
            logger.error(
                {"error": "Note object update failed", "errors": repr(e)},
            )
            return False

    def delete_object(self) -> bool:
        try:
            self.is_active = False
            self.deleted_at = timezone.now()
            self.save()
            return True
        except Exception as e:
            logger.error(
                {"error": "Note object delete failed", "errors": repr(e)},
            )
            return False
