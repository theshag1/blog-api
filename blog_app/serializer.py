from rest_framework import serializers
from .models import Blog, LikeDislike, Comment


class BlogSerializer(serializers.ModelSerializer):
    class Meta:
        model = Blog
        fields = (
        'title', 'slug', 'author', 'blog_body', 'image_or_video', 'category', 'created_at', 'blog_interesting')
        read_only_fields = ('id',)


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('blog', 'user', 'body')
        read_only_fields = ('id',)


class LikeDislikeSerializer(serializers.Serializer):
    type = serializers.ChoiceField(choices=LikeDislike.LikeType.choices)
