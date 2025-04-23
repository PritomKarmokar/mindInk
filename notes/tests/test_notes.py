from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework.views import status
from rest_framework.test import APITestCase

from notes.models import Note

User = get_user_model()


class BaseViewTest(APITestCase):
    def setUp(self):
        self.user_data = {
            "email": "testuser@gmail.com",
            "username": "testuser",
            "password": "test123",
        }
        self.signup()
        self.login_user()
        self.user = self.get_user_instance()
        self.note_object = self.create_note("Golang", "Adding CheatSheet", self.user)

    def signup(self):
        response = self.client.post(
            reverse("signup"),
            data=self.user_data,
        )
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def login_user(self):
        response = self.client.post(
            reverse("login"),
            data={
                "email": self.user_data["email"],
                "password": self.user_data["password"],
            },
        )

        # print(response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        token = response.json()["access_token"]
        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def get_user_instance(self):
        return User.objects.get(username=self.user_data["username"])

    def create_note(self, title: str, content: str, user: User):
        if title and content and user:
            return Note.objects.create(title=title, content=content, user=user)


class NotesCreateListAPITestCase(BaseViewTest):
    def setUp(self):
        super().setUp()
        self.url = reverse("notes-create-or-list")

    def test_create_note(self):
        payload = {
            "title": "Test Note",
            "content": "This is a test content",
        }
        response = self.client.post(self.url, payload)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 2)

    def test_list_notes(self):
        response = self.client.get(self.url)
        # print(f"response.data: {response.data}")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class NotesRetrieveUpdateDeleteAPITestCase(BaseViewTest):
    def setUp(self):
        super().setUp()
        self.url = reverse(
            "notes-retrieve-update-delete", kwargs={"note_id": self.note_object.id}
        )

    def test_retrieve_note(self):
        response = self.client.get(
            self.url,
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]["title"], "Golang")

    def test_update_note(self):
        new_title = {
            "title": "Golang Updated",
        }

        response = self.client.patch(self.url, new_title)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.note_object.refresh_from_db()  # reloads the note object from the DB after patch
        self.assertEqual(self.note_object.title, new_title["title"])

    def test_delete_note(self):
        response = self.client.delete(self.url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
