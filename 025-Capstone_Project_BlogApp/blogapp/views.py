from django.shortcuts import render
from rest_framework import viewsets
# from rest_framework.permissions import DjangoModelPermissions

from .models import (
    Profile,
    Category,
    Post,
    Comment, 
    Like, 
    PostVN,
)
from .serializers import (
    ProfileSerializer,
    CategorySerializer,
    PostSerializer,
    CommentSerializer,
    LikeSerializer,
    PostVNSerializer,
)


# Post/:
class PostView(viewsets.ModelViewSet):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    # permission_classes = [DjangoModelPermissions]
    # permission_classes = [IsStaffPermission] # Only StaffUser

class ProfileView(viewsets.ModelViewSet):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    # permission_classes = [DjangoModelPermissions]

class CategoryView(viewsets.ModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    # permission_classes = [DjangoModelPermissions]

class CommentView(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    # permission_classes = [DjangoModelPermissions]

class LikeView(viewsets.ModelViewSet):
    queryset = Like.objects.all()
    serializer_class = LikeSerializer
    # permission_classes = [DjangoModelPermissions]

class PostVNView(viewsets.ModelViewSet):
    queryset = PostVN.objects.all()
    serializer_class = PostVNSerializer
    # permission_classes = [DjangoModelPermissions]
