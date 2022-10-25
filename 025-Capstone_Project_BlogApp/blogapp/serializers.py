from django.contrib.auth.models import User
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

    like= LikeSerializer(many=True, read_only= True)
    comment=CommentSerializer(many=True, read_only= True)
    views=PostVNSerializer(many=True, read_only= True)
    user=serializers.StringRelatedField()
    user_id=serializers.IntegerField(write_only=True)
    category_name=serializers.SerializerMethodField()
    status_name=serializers.SerializerMethodField() # bu ikinci ve uzun yöntem
    # status=serializers.CharField(source="get_status_display")

    class Meta:
        model = Post
        # fields = '__all__'
        fields = (
            "id",
            "user",
            "user_id",
            "category",
            "category_name", 
            "title", 
            "content", 
            "image_url", 
            "publish_date", 
            "last_updated", 
            "status",
            "status_name",
            "like",
            "comment",
            "views",
        )
    def get_status_name(self, object):               # choises oldugu zaman bu sekilde isimler görunebilir. get_  dan sonra modeldeki field name olacak, sonrada _display
        return object.get_status_display()

    def get_category_name(self, object):
        return Category.objects.get(name=object.category).name

    # def create (self, validated_data):
    #     user = User.objects.get(username=validated_data["user"])
    #     validated_data["user"] = user.id
    #     return Post.objects.create(**validated_data)