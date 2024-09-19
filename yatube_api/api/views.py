from django.shortcuts import get_object_or_404
from rest_framework import serializers, viewsets
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import IsAuthenticated

from posts.models import Follow, Group, Post
from .permissions import ReadOnlyOrAuthorPermissions
from .serializers import (CommentSerializer,
                          FollowSerializer,
                          PostSerializer,
                          GroupSerializer)


class PostViewSet(viewsets.ModelViewSet):
    """
    Возвращает список всех постов, также
    реализует СRUD операции с постами.
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [ReadOnlyOrAuthorPermissions]
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """
    Возвращает список всех групп и конкретную
    группу по ID.
    """
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [ReadOnlyOrAuthorPermissions]


class CommentViewSet(viewsets.ModelViewSet):
    """
    Возвращает список всех комментариев, также
    реализует СRUD операции с комментариями.
    """
    serializer_class = CommentSerializer
    permission_classes = [ReadOnlyOrAuthorPermissions]

    def get_post(self):
        if self.kwargs['post_id'] is None:
            raise ValueError('ID поста не обнаружен!')
        return get_object_or_404(Post, pk=self.kwargs['post_id'])

    def get_queryset(self):
        return self.get_post().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, post=self.get_post())


class FollowViewSet(viewsets.ModelViewSet):
    """Возвращает список подписок пользователя."""
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        search = self.request.query_params.get('search', None)
        queryset = Follow.objects.filter(user=self.request.user)
        return (queryset.filter(following__username=search)
                if search else queryset)

    def perform_create(self, serializer):
        following_user = serializer.validated_data['following']
        if Follow.objects.filter(
            user=self.request.user,
            following=following_user
        ).exists() or following_user == self.request.user:
            raise serializers.ValidationError('Вы уже подписаны или'
                                              'пытаетесь подписаться на себя!')
        serializer.save(user=self.request.user)
