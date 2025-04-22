from django.contrib import admin

from notes.models import Note


@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = (
        "title",
        "content",
        "user",
    )
    ordering = ("-created_at",)
    search_fields = ("title",)

    readonly_fields = ("created_at", "updated_at")
