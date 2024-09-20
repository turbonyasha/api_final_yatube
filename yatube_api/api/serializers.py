from django.contrib.auth import get_user_model

from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from posts.models import Comment, Follow, Group, Post

User = get_user_model()


class PostSerializer(serializers.ModelSerializer):
    author = SlugRelatedField(slug_field='username', read_only=True)

    class Meta:
        fields = '__all__'
        model = Post


class CommentSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(
        read_only=True, slug_field='username'
    )

    class Meta:
        fields = '__all__'
        read_only_fields = ('post',)
        model = Comment


class FollowSerializer(serializers.ModelSerializer):
    user = serializers.CharField(source='user.username', read_only=True)
    following = serializers.SlugRelatedField(
        slug_field='username',
        queryset=User.objects.all(),
        required=True
    )

    def validate(self, attrs):
        following = attrs.get('following')
        if self.context['request'].user == following:
            raise serializers.ValidationError(
                'Вы не можете подписаться на самого себя.'
            )
        if Follow.objects.filter(
            user=self.context['request'].user, following=following
        ).exists():
            raise serializers.ValidationError(
                'Вы уже подписаны на этого пользователя.'
            )
        return attrs

    class Meta:
        fields = '__all__'
        model = Follow


class GroupSerializer(serializers.ModelSerializer):

    class Meta:
        fields = '__all__'
        model = Group
