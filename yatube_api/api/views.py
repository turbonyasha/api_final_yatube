from django.shortcuts import get_object_or_404
from rest_framework import permissions, viewsets
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from posts.models import Follow, Group, Post
from .serializers import (CommentSerializer,
                          FollowSerializer,
                          PostSerializer,
                          GroupSerializer)
from .pagination import CustomPagination


class ReadOnlyOrAuthorPermissions(permissions.BasePermission):
    """Класс, определяющий предоставленные разрешения."""

    def has_permission(self, request, view):
        return (
            request.method in permissions.SAFE_METHODS
            or request.user.is_authenticated
        )

    def has_object_permission(self, request, view, obj):
        return (request.method in permissions.SAFE_METHODS
                or obj.author == request.user)


class PostViewSet(viewsets.ModelViewSet):
    """Представление модели Post."""
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [ReadOnlyOrAuthorPermissions]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Представление модели Group."""
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [ReadOnlyOrAuthorPermissions]

    def list(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)


class CommentViewSet(viewsets.ModelViewSet):
    """Представление модели Comment."""
    serializer_class = CommentSerializer
    permission_classes = [ReadOnlyOrAuthorPermissions]

    def get_post(self):
        if self.kwargs['post_id'] is None:
            raise ValueError('ID поста не обнаружен!')
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments.all()

    def list(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(viewsets.ModelViewSet):
    """Представление модели FollowersUser."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)
    
    def list(self, request, *args, **kwargs):
        return Response(self.get_serializer(self.get_queryset(), many=True).data)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
