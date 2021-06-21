from django.urls import path

from api.views import PostApiview, PostDetailview, PostDeleteApiview, PostUpdateApiview

urlpatterns = [
    path('posts/', PostApiview.as_view(), name='blog-api'),
    path('posts/<int:pk>', PostDetailview.as_view(), name='blog-detail'),
    path('posts/delete/<int:pk>', PostDeleteApiview.as_view(), name='blog-delete'),
    path('posts/update/<int:pk>', PostUpdateApiview.as_view(), name='blog-update'),
]
