from django.urls import path
from .views import (
    StudentListView,
    StudentDetailView,
    StudentView,
    StudentDetail,
    StudetListCreate,
    StudentRUD,
    StudentCRUD
)

from rest_framework import routers

router = routers.DefaultRouter()
router.register('student', StudentCRUD)

urlpatterns = [
    # path('student/', StudentListView.as_view()),
    # path('student/', StudentView.as_view()),
    # path('student/', StudetListCreate.as_view()),
    # path('student_detail/<int:pk>', StudentDetailView.as_view())
    # path('student_detail/<int:pk>', StudentDetail.as_view())
    # path('student_detail/<int:pk>', StudentRUD.as_view())
]

urlpatterns += router.urls
