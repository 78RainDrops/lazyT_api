from django.urls import path
from .views import TaskList, TaskDetails, Register, Login

urlpatterns = [
    path("task/", TaskList.as_view(), name="task"),
    path("task/<int:pk>/", TaskDetails.as_view(), name="Task details"),
    path("accounts/register/", Register.as_view(), name="register"),
    path("accounts/login/", Login.as_view(), name="login"),
]
