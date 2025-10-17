from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Task(models.Model):
    title = models.CharField(max_length=255)
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="tasks",
    )
    description = models.TextField(default=True)
    is_completed = models.BooleanField(default=False)
    priority = models.CharField(
        max_length=255,
        choices=[("low", "Low"), ("medium", "Medium"), ("high", "High")],
        default="medium",
        db_index=True,
    )
    due_date = models.DateField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["priority"]),
            models.Index(fields=["is_completed"]),
        ]

    def __str__(self):
        return f"{self.title} - {self.user.username}"
