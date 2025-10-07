from django.urls import path
from .views import TaskList, TaskDetails

urlpatterns = [
    path("task/", TaskList.as_view(), name="task"),
    path("task/<int:pk>/", TaskDetails.as_view(), name="Task details"),
]
