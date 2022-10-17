from django.contrib import admin
from .models import Profile, Category, Post, Comment, Like, PostVN

admin.site.register(Profile)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostVN)
admin.site.register(Comment)
admin.site.register(Like)
