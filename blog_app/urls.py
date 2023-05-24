from django.urls import path

from .views import BlogApiView ,BlogApiDetilView ,BlogLikeDislikeView ,BlogCommentView , Top20View

urlpatterns = [
    path('', BlogApiView.as_view(), name='blog-api'),
    path('<int:pk>', BlogApiDetilView.as_view(), name='blog-api'),
    path('<int:pk>/like/', BlogLikeDislikeView.as_view(), name='blog-like'),
    path('<int:pk>/comment/', BlogCommentView.as_view(), name='blog-comment'),
    path('top20', Top20View.as_view(), name='blog-top'),

]
