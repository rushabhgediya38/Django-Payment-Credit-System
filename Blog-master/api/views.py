from django.shortcuts import render
from rest_framework.generics import ListAPIView, RetrieveAPIView, DestroyAPIView, UpdateAPIView
from blog.models import Post
from .serializers import PostSerializer, PostDetailSerializer

# Create your views here.


class PostApiview(ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostDetailview(RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # lookup_field = 'title'
    # lookup_url_kwarg = 'abc'


class PostDeleteApiview(DestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer


class PostUpdateApiview(UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostDetailSerializer