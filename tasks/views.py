from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import ValidationError, NotFound, AuthenticationFailed
from rest_framework import status
from django.contrib.auth.hashers import check_password
from django.contrib.auth.models import User
from django.db.models import Q
from .serializers import TaskSerializer, UserSerializer
from .models import Task
from .utils import generate_token

# Create your views here.


class TaskList(APIView):
    def get(self, request):
        task = (
            Task.objects.filter(user=request.user)
            .select_related("user")
            .order_by("-created_at")
        )

        # Filter
        completed = request.query_params.get("completed")
        priority = request.query_params.get("priority")

        if completed is not None:
            completed = completed.lower()
            if completed in ["true", "1", "yes"]:
                task = task.filter(is_completed=True)
            elif completed in ["false", "0", "no"]:
                task = task.filter(is_completed=False)

        if priority:
            task = task.filter(priority__iexact=priority)

        # search
        search = request.query_params.get("search")
        if search:
            task = task.filter(
                Q(title__icontains=search) | Q(description__icontains=search)
            )

        paginator = PageNumberPagination()
        paginator_task = paginator.paginate_queryset(task, request)
        serializer = TaskSerializer(paginator_task, many=True)
        # return Response(serializer.data)
        return paginator.get_paginated_response(serializer.data)

    def post(self, request):
        serializer = TaskSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)


class TaskDetails(APIView):
    def get_object(self, pk, user):
        try:
            return Task.objects.get(pk=pk, user=user)
        except Task.DoesNotExist:
            raise NotFound("Task Not Found")

    def get(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            raise NotFound("Task Not Found")
        serializer = TaskSerializer(task)
        return Response(serializer.data)

    def put(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            raise NotFound("Task Not Found")
        serializer = TaskSerializer(task, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        raise ValidationError(serializer.errors)

    def delete(self, request, pk):
        task = self.get_object(pk, request.user)
        if not task:
            raise NotFound("Task Not Found")
        task.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class Register(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        raise ValidationError(serializer.errors)


class Login(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get("username")
        password = request.data.get("password")
        if not username or not password:
            raise AuthenticationFailed("Username and password are required.")

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            raise AuthenticationFailed("Invalid Username or Password")

        if not check_password(password, user.password):
            raise AuthenticationFailed("Invalid Username or Password")
        token = generate_token(user.id)
        return Response({"token": token}, status=status.HTTP_200_OK)
