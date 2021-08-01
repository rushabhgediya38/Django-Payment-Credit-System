from django.urls import path
from . import views
from blog.views import (PostListView,
                        PostDetailView,
                        PostUpdateView,
                        PostDeleteView,
                        UserPostListView,
                        AddCommentView,
                        )

from .views import post_create1
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('', PostListView.as_view(), name='blog-home'),
    path('user/<str:username>', UserPostListView.as_view(), name='user-posts'),
    path('post/<int:pk>/', PostDetailView.as_view(template_name='blog/post_detail.html'), name='post-detail'),
    path('post/<int:pk>/comment/', AddCommentView.as_view(template_name='blog/add_comment.html'), name='post_comment'),
    path('post/<int:pk>/update/', PostUpdateView.as_view(), name='post-update'),
    path('post/<int:pk>/delete/', PostDeleteView.as_view(template_name='blog/post_confirm_delete.html'),
         name='post-delete'),
    # path('post/new/', PostCreateView.as_view(template_name='blog/post_form.html'), name='post-create'),
    path('about/', views.about, name='blog-about'),
    path('post/post_create/', post_create1, name='post_create'),

    path('credit/points/', views.CPoints, name='credit_points'),
    path('credit/points/<str:plans>/', views.CPointsPlans, name='CPointsPlans'),
    path('BronzePlan', views.BronzePlan, name='BronzePlan'),
    path('SilverPlan', views.SilverPlan, name='SilverPlan'),
    path('GoldPlan', views.GoldPlan, name='GoldPlan'),
    path('premium-data/', views.premium_data, name='premium-data'),
    path('StartupSubmissionListTestesing/', csrf_exempt(views.StartupSubmissionListTestesing), name='StartupSubmissionListTestesing')

]
