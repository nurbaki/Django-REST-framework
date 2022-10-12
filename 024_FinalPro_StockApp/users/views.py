from django.shortcuts import render
from rest_framework.generics import CreateAPIView

from django.contrib.auth.models import User
from .serializers import RegisterSerializer
from users import serializers

class RegisterView(CreateAPIView):

    queryset = User.objects.all()
    serializer_class = RegisterSerializer

    # for publish special messages:
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            from rest_framework.response import Response
            return Response({
                "status": True,
                "message": "User created",
                "username": request.data["username"],
                "email": request.data["email"],
                "first_name": request.data.get("first_name"),
                "last_name": request.data.get("last_name"),
            })