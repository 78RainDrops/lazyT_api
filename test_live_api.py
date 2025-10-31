import requests

BASE_URL = "https://lazyt-api.onrender.com/api"


def test_register_user():
    print("\n Testing Register Endpoint...")
    data = {
        "username": "testuser_live",
        "password": "StrongPass123",
        "email": "liveuser@example.com",
    }
    response = requests.post(f"{BASE_URL}/accounts/register/", json=data)
    print("Status:", response.status_code)
    print("Response:", response.json())


def test_login_user():
    print("\n Testing Login Endpoint...")
    data = {"username": "testuser_live", "password": "StrongPass123"}
    response = requests.post(f"{BASE_URL}/accounts/login/", json=data)
    print("Status:", response.status_code)
    print("Response:", response.json())
    if response.status_code == 200 and "token" in response.json():
        return response.json()["token"]
    return None


def test_create_task(token):
    print("\n Testing Create Task Endpoint")
    headers = {"Authorization": f"Bearer {token}"}
    data = {
        "title": "Live API Task with due date",
        "description": "Testing live deployment with due date",
        "priority": "high",
        "due_date": "2025-10-29",
    }

    response = requests.post(f"{BASE_URL}/task/", json=data, headers=headers)
    print("Status:", response.status_code)
    print("Response:", response.json())


if __name__ == "__main__":
    test_register_user()
    token = test_login_user()
    if token:
        test_create_task(token)
    else:
        print("\n No Token retrieved - login may have failed.")
