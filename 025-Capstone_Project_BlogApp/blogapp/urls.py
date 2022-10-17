from rest_framework import routers
from django.conf.urls.static import static
from django.conf import settings
from .views import (
    PostView,
    ProfileView,
    CategoryView,
    LikeView,
    CommentView,
    PostVNView,
)

router = routers.DefaultRouter()
router.register('posts', PostView)
router.register('profiles', ProfileView)
router.register('category', CategoryView)
router.register('likes', LikeView)
router.register('comments', CommentView)
router.register('views', PostVNView)

urlpatterns = router.urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)