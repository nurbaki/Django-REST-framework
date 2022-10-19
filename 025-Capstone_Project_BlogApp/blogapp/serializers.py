from unicodedata import category
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

class CommentSerializer(serializers.ModelSerializer):

    user=serializers.StringRelatedField()

    class Meta:
        model = Comment
        fields = '__all__'

class LikeSerializer(serializers.ModelSerializer):

    user=serializers.StringRelatedField()

    class Meta:
        model = Like
        #fields = '__all__'
        exclude = (
          "id",
          "post",
        )

class PostVNSerializer(serializers.ModelSerializer):

    class Meta:
        model = PostVN
        #fields = '__all__'
        exclude = (
          "id",
          #"post",
          "user",
        )

class PostSerializer(serializers.ModelSerializer):

    like= LikeSerializer(many=True)
    comment=CommentSerializer(many=True)
    views=PostVNSerializer(many=True)
    user=serializers.StringRelatedField()
    category=serializers.StringRelatedField()
    # status=serializers.SerializerMethodField() # bu ikinci ve uzun yöntem
    status=serializers.CharField(source="get_status_display")

    class Meta:
        model = Post
        # fields = '__all__'
        fields = (
            "id",
            "user",
            "category", 
            "title", 
            "content", 
            "image_url", 
            "publish_date", 
            "last_updated", 
            "status",
            "like",
            "comment",
            "views",
        )
    # def get_status(self, object):               # choises oldugu zaman bu sekilde isimler görunebilir. get_  dan sonra modeldeki field name olacak, sonrada _display
    #     return object.get_status_display()