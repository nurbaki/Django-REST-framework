from django.urls import path, include
from .views import RegisterView

# after 'users/':
urlpatterns = [
    # redirect all auth process to dj_rest_auth:
    path('auth/', include('dj_rest_auth.urls')),
    path('register/', RegisterView.as_view()),
]