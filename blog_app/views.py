from django.http import Http404
from django_filters.rest_framework import DjangoFilterBackend
from drf_yasg.utils import swagger_auto_schema
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from blog_app.models import Blog, LikeDislike, Comment
from blog_app.serializer import BlogSerializer, LikeDislikeSerializer, CommentSerializer
from paginations import CustomPageNumerPagination


# Create your views here.

class BlogApiView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    filter_backends = (DjangoFilterBackend, OrderingFilter, SearchFilter)
    filterset_fields = ("category", "blog_interesting")
    search_fields = ('title', 'author')
    pagination_class = CustomPageNumerPagination

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return BlogSerializer
        return BlogSerializer


class BlogApiDetilView(generics.RetrieveUpdateAPIView):
    queryset = Blog.objects.all()

    def get_serializer_class(self):
        if self.request.method == 'PUT' or self.request.method == 'PATCH':
            return BlogSerializer
        return BlogSerializer


class BlogLikeDislikeView(APIView):
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=LikeDislikeSerializer)
    def post(self, request, *args, **kwargs):
        serializer = LikeDislikeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        type_ = serializer.validated_data.get('type')
        user = request.user

        blog = Blog.objects.filter(id=self.kwargs.get('pk')).first()
        if not blog:
            raise Http404
        like_dislike_blog = LikeDislike.objects.filter(blog=blog, user=user).first()
        if like_dislike_blog and like_dislike_blog.type == type_:
            like_dislike_blog.delete()
        else:
            LikeDislike.objects.update_or_create(blog=blog, user=user, defaults={'type': type_})
            data = {'type': type_, "detail": "Liked or disliked"}
        return Response(data)


class BlogCommentView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, requset, *args, **kwargs):
        blog = Blog.objects.filter(id=self.kwargs.get('pk')).first()
        data_comments = Comment.objects.filter(blog=blog)
        serializer = BlogSerializer(data_comments, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(request_body=CommentSerializer)
    def post(self, request, *args, **kwargs):
        serializer = BlogSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        body = serializer.validated_data.get('body')
        user = request.user
        blog = Blog.objects.filter(id=self.kwargs.get('pk')).first()
        if not blog:
            raise Http404
        Comment.objects.update_or_create(blog=blog, user=user, body=body)
        data = {'blog': blog}
        return Response(data)


class Top20View(generics.ListAPIView):
    queryset = Blog.objects.order_by('-created_at')[:20]
    serializer_class = BlogSerializer


class BLogUserInterestingView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        interesting = user.interesting
        user_blog = Blog.objects.filter(blog_interesting=interesting)
        serializer = BlogSerializer(user_blog, many=True)

        return Response(serializer.data)
