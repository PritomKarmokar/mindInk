from django.urls import reverse

from rest_framework.test import APITestCase
from rest_framework.views import status

from .models import Note
from .serializers import NoteSerializer


class BaseViewTest(APITestCase):
    def setUp(self):
        self.url = reverse("notes-create-or-list")
        self.authenticate_user()

    def authenticate_user(self):
        signup_response = self.client.post(
            reverse("signup"),
            data={
                "email": "testuser@gmail.com",
                "username": "testuser",
                "password": "test123",
            },
        )
        print(signup_response.data)

        login_response = self.client.post(
            reverse("login"),
            data={"email": "testuser@gmail.com", "password": "test123"},
        )
        print(login_response.data)

        token = login_response.data["access_token"]

        self.client.credentials(HTTP_AUTHORIZATION=f"Bearer {token}")

    def test_create_note(self):
        new_note = {
            "title": "Test note",
            "content": "Test content",
        }
        response = self.client.post(self.url, data=new_note)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Note.objects.count(), 1)
