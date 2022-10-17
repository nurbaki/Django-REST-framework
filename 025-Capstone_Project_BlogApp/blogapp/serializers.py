from rest_framework import serializers
from .models import (
    Profile,
    Category,
    Post,
    Comment, 
    Like, 
    PostVN,
)

class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = Profile
        fields = '__all__'

class CategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = Category
        fields = '__all__'

class PostSerializer(serializers.ModelSerializer):

    class Meta:
        model = Post
        #fields = '__all__'
        exclude = (
            "user",
        )

class CommentSerializer(serializers.ModelSerializer):

    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Like
        fields = '__all__'

class PostVNSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostVN
        fields = '__all__'