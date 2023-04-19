from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse
from rest_framework import viewsets
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.views import APIView

from core.models import User, Post, Comment
from core.permissions import IsUserOwner, IsPostOwner, IsCommentOwner
from core.serializers import UserLoginSerializer, UserCreateUpdateDestroySerializer, UserListRetrieveSerializer, \
    PostListRetrieveSerializer, PostCreateUpdateDestroySerializer, CommentListRetrieveSerializer, \
    CommentCreateUpdateDestroySerializer


# Create your views here.


class AuthView(APIView):
    serializer_class = UserLoginSerializer
    def post(self, request):
        user_login = request.data["login"]
        password = request.data["password"]
        user = authenticate(request, login=user_login, password=password)
        if user is not None:
            login(request, user)
        else:
            return JsonResponse({"Status": "Wrong password or login"})
        return JsonResponse({"Status": "Successfully logged in"})

    def delete(self, request):
        logout(request)
        return JsonResponse({"Status": "Successfully logout"})


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    http_method_names = ["get", "post", "put", 'delete']

    serializer_classes = {
        'create': UserCreateUpdateDestroySerializer,
        'list': UserListRetrieveSerializer,
        'retrieve': UserListRetrieveSerializer,
        'update': UserCreateUpdateDestroySerializer,
        'destroy': UserCreateUpdateDestroySerializer,
    }

    permission_classes_by_action = {
        'list': [IsAdminUser | IsAuthenticated],
        'retrieve': [IsAdminUser | IsAuthenticated],
        'create': [AllowAny],
        'update': [IsAdminUser | IsUserOwner],
        'destroy': [IsAdminUser],
    }

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    http_method_names = ["get", "post", "put", 'delete']

    serializer_classes = {
        'create': PostCreateUpdateDestroySerializer,
        'list': PostListRetrieveSerializer,
        'retrieve': PostListRetrieveSerializer,
        'update': PostCreateUpdateDestroySerializer,
        'destroy': PostCreateUpdateDestroySerializer,
    }

    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAdminUser | IsPostOwner],
        'destroy': [IsAdminUser | IsPostOwner],
    }

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    http_method_names = ["get", "post", "put", 'delete']

    serializer_classes = {
        'create': CommentCreateUpdateDestroySerializer,
        'list': CommentListRetrieveSerializer,
        'retrieve': CommentListRetrieveSerializer,
        'update': CommentCreateUpdateDestroySerializer,
        'destroy': CommentCreateUpdateDestroySerializer,
    }

    permission_classes_by_action = {
        'list': [AllowAny],
        'retrieve': [AllowAny],
        'create': [IsAuthenticated],
        'update': [IsAdminUser | IsCommentOwner],
        'destroy': [IsAdminUser | IsCommentOwner],
    }

    def get_permissions(self):
        return [permission() for permission in self.permission_classes_by_action[self.action]]

    def get_serializer_class(self):
        return self.serializer_classes.get(self.action)
