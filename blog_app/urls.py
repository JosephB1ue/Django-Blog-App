from django.urls import path
from .views import register_page, login_page, post_list_page, post_detail_page
from .views import (
    PostListCreateView, PostDetailView, PostLikeToggle,
    CommentListCreateView, CommentDetailView, register, login, logout
)

urlpatterns = [
    # API routes (put these first to avoid conflicts)
    path('auth/register/', register, name='register'),
    path('auth/login/', login, name='login'),
    path('auth/logout/', logout, name='logout'),
    path('posts/', PostListCreateView.as_view(), name='post-list-create'),
    path('posts/<int:pk>/', PostDetailView.as_view(), name='post-detail'),
    path('posts/<int:pk>/like/', PostLikeToggle.as_view(), name='post-like-toggle'),
    path('posts/<int:post_pk>/comments/', CommentListCreateView.as_view(), name='comment-list-create'),
    path('comments/<int:pk>/', CommentDetailView.as_view(), name='comment-detail'),
    
    # Page routes (put these last)
    path('', post_list_page, name='post-list-page'),
    path('view/posts/<int:post_id>/', post_detail_page, name='post-detail-page'),
    path('register/', register_page, name='register-page'),
    path('login/', login_page, name='login-page'),
]
