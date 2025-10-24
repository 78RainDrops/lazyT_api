from django.contrib.auth.models import User
from tasks.utils import generate_token
from rest_framework.test import APITestCase, APIClient
from rest_framework import status
from .models import Task
import time
from django.test import TestCase


def create_test_user(
    username="testuser", password="testpass", email="test@example.com"
):
    return User.objects.create_user(username=username, password=password, email=email)


def create_test_token(user):
    return generate_token(user.id)


# Create your tests here.
class TaskCRUDTests(APITestCase):
    def setUp(self):
        # Create test user
        # self.user = User.objects.create_user(
        #     username="testuser", password="testpass123"
        # )
        self.user = create_test_user()

        # Authenticate User
        self.client = APIClient()
        self.client.force_authenticate(user=self.user)

        # create a sample task
        self.task = Task.objects.create(
            user=self.user,
            title="Initial Task",
            description="Test description",
            priority="medium",
        )

    def test_create_task(self):
        data = {
            "title": "New Task",
            "description": "create in test",
            "priority": "high",
        }
        response = self.client.post("/api/task/", data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Task.objects.count(), 2)

        # last_task = Task.objects.last()
        # self.assertIsNotNone(last_task)
        # self.assertEqual(last_task.title, "New Task")
        create_task = Task.objects.get(title="New Task")
        self.assertEqual(create_task.description, "create in test")

    def test_get_tasks(self):
        response = self.client.get("/api/task/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("results", response.data)  # Since pagination
        self.assertGreaterEqual(len(response.data["results"]), 1)

    def test_get_single_task(self):
        response = self.client.get(f"/api/task/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.task.title)

    def test_update_task(self):
        data = {
            "title": "Updated Task",
            "description": "Updated description",
            "priority": "low",
        }
        response = self.client.put(
            f"/api/task/{self.task.id}/",
            data,
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.task.refresh_from_db()
        self.assertEqual(self.task.title, "Updated Task")

    def test_delete_task(self):
        response = self.client.delete(f"/api/task/{self.task.id}/")
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Task.objects.filter(id=self.task.id).exists())

    def test_get_nonexistent_task(self):
        response = self.client.get("/api/task/999/")
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertIn("error", response.data)


class TaskJWTAuthTests(APITestCase):
    def setUp(self):
        # self.user = User.objects.create_user(username="jwtuser", password="testpass")
        self.user = create_test_user(username="jwtuser")
        # self.token = generate_token(self.user.id)
        self.token = create_test_token(self.user)
        self.auth_header = {"HTTP_AUTHORIZATION": f"Bearer {self.token}"}

    def test_access_without_token(self):
        response = self.client.get("/api/task/")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_valid_token(self):
        response = self.client.get("/api/task/", **self.auth_header)
        self.assertNotEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_access_with_invalid_token(self):
        response = self.client.get(
            "/api/task/",
            HTTP_AUTHORIZATION="Bearer invalid_token_123",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_expired_token(self):
        from datetime import datetime, timedelta, timezone
        import jwt
        from django.conf import settings

        short_exp_payload = {
            "user_id": self.user.id,
            "exp": datetime.now(timezone.utc) - timedelta(seconds=1),
            "iat": datetime.now(timezone.utc),
        }
        expired_token = jwt.encode(
            short_exp_payload, settings.SECRET_KEY, algorithm="HS256"
        )
        response = self.client.get(
            "/api/task/",
            HTTP_AUTHORIZATION=f"Bearer {expired_token}",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class AuthRouteTests(APITestCase):
    def setUp(self):
        self.register_url = "/api/accounts/register/"
        self.login_url = "/api/accounts/login/"
        self.user_data = {
            "username": "testuser",
            "email": "test@example.com",
            "password": "securepassword123",
        }
        User.objects.create_user(**self.user_data)

    def test_register_user_success(self):
        data = {
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword123",
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn("id", response.data)
        self.assertEqual(response.data["username"], data["username"])

    def test_register_existing_username(self):
        response = self.client.post(self.register_url, self.user_data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("username", str(response.data).lower())

    def test_login_success(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)
        self.assertTrue(len(response.data["token"]) > 10)

    def test_login_wrong_password(self):
        response = self.client.post(
            self.login_url,
            {"username": self.user_data["username"], "password": "wrongpassword"},
            format="json",
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)
        self.assertIn("error", response.data["status"])

    def test_login_nonexistent_user(self):
        response = self.client.post(
            self.login_url, {"username": "ghost", "password": "whatever"}, format="json"
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_login_then_access_task(self):
        response = self.client.post(
            self.login_url,
            {
                "username": self.user_data["username"],
                "password": self.user_data["password"],
            },
            format="json",
        )
        token = response.data.get("token")
        self.assertIsNotNone(token)
        task_response = self.client.get(
            "/api/task/", HTTP_AUTHORIZATION=f"Bearer {token}"
        )
        self.assertIn(task_response.status_code, [200, 204])


class IsolationCheck(TestCase):
    def test_first(self):
        User.objects.create(username="alpha")
        self.assertEqual(User.objects.count(), 1)

    def test_second(self):
        self.assertEqual(User.objects.count(), 0)
