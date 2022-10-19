from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    bio = models.CharField(max_length=500, blank=True)
    image = models.ImageField(upload_to='profile_pic', default="avatar1.jpg")

    def __str__(self):
        return self.user.username

class Category(models.Model):

    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class Post(models.Model):
    Status =(
        ("1", "Draft"),
        ("2", "Published"),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    content = models.TextField()
    image_url = models.URLField(blank=True, null=True)
    publish_date = models.DateField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=50, choices=Status)

    def __str__(self):
        return self.title

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= "comment")
    time_stamp = models.DateField(auto_now_add=True)
    content = models.TextField()

class Like(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= "like")

class PostVN(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name= "views")
    view_number = models.IntegerField(blank=True, null=True)