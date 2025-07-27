from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator

from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Post, Comment
from .serializers import PostSerializer, CommentSerializer

from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token
from django.contrib.auth import authenticate
from rest_framework.decorators import api_view, permission_classes
from django.core.exceptions import PermissionDenied
from rest_framework.permissions import AllowAny
from rest_framework import status

@method_decorator(csrf_exempt, name='dispatch')
class PostListCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all().order_by('-created_at')
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

@method_decorator(csrf_exempt, name='dispatch')
class PostDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        print(f"Update request from user: {self.request.user}")
        print(f"Post author: {self.get_object().author}")
        if self.request.user != self.get_object().author:
            raise PermissionDenied("You can only edit your own posts.")
        serializer.save()

    def perform_destroy(self, instance):
        print(f"Delete request from user: {self.request.user}")
        print(f"Post author: {instance.author}")
        if self.request.user != instance.author:
            raise PermissionDenied("You can only delete your own posts.")
        instance.delete()

    def update(self, request, *args, **kwargs):
        print(f"Update method called for post {kwargs.get('pk')}")
        print(f"Request method: {request.method}")
        print(f"Request user: {request.user}")
        print(f"Request headers: {dict(request.headers)}")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        print(f"Destroy method called for post {kwargs.get('pk')}")
        print(f"Request method: {request.method}")
        print(f"Request user: {request.user}")
        print(f"Request headers: {dict(request.headers)}")
        return super().destroy(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class PostLikeToggle(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self, request, pk):
        post = Post.objects.get(pk=pk)
        if request.user in post.likes.all():
            post.likes.remove(request.user)
            liked = False
        else:
            post.likes.add(request.user)
            liked = True
        return Response({'liked': liked, 'likes_count': post.likes.count()})

@method_decorator(csrf_exempt, name='dispatch')
class CommentListCreateView(generics.ListCreateAPIView):
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_queryset(self):
        return Comment.objects.filter(post_id=self.kwargs['post_pk'])

    def perform_create(self, serializer):
        print(f"Creating comment for post {self.kwargs['post_pk']}")
        print(f"Comment author: {self.request.user}")
        print(f"Comment text: {serializer.validated_data.get('text')}")
        serializer.save(author=self.request.user, post_id=self.kwargs['post_pk'])

    def create(self, request, *args, **kwargs):
        print(f"Create comment request for post {kwargs.get('post_pk')}")
        print(f"Request method: {request.method}")
        print(f"Request user: {request.user}")
        print(f"Request data: {request.data}")
        return super().create(request, *args, **kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class CommentDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def perform_update(self, serializer):
        if self.request.user != self.get_object().author:
            raise PermissionDenied("You can only edit your own comments.")
        serializer.save()

    def perform_destroy(self, instance):
        if self.request.user != instance.author:
            raise PermissionDenied("You can only delete your own comments.")
        instance.delete()

def register_page(request):
    return render(request, 'blog_app/register.html')

def login_page(request):
    return render(request, 'blog_app/login.html')

def post_list_page(request):
    return render(request, 'blog_app/post_list.html')

def post_detail_page(request, post_id):
    return render(request, 'blog_app/post_detail.html')

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def register(request):
    username = request.data.get('username')
    password = request.data.get('password')
    if not username or not password:
        return Response({'error': 'Username and password required.'}, status=status.HTTP_400_BAD_REQUEST)
    if User.objects.filter(username=username).exists():
        return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)
    user = User.objects.create_user(username=username, password=password)
    token, created = Token.objects.get_or_create(user=user)
    return Response({'token': token.key, 'username': user.username})

@csrf_exempt
@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(username=username, password=password)
    if user is not None:
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key, 'username': user.username})
    else:
        return Response({'error': 'Invalid credentials'}, status=status.HTTP_400_BAD_REQUEST)

@csrf_exempt
@api_view(['POST'])
def logout(request):
    request.user.auth_token.delete()
    return Response({'success': 'Logged out'})
