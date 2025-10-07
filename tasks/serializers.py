from rest_framework import serializers
from .models import Task


class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = "__all__"
        read_only_fields = ["id", "created_at", "updated_at"]
        # fields = [
        #     "id",
        #     "title",
        #     "description",
        #     "is_completed",
        #     "priority",
        #     "due_date",
        #     "created_at",
        #     "updated_at",
        # ]
