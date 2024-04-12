from django.shortcuts import render
from rest_framework import viewsets, generics
from outlinecompilation.models import User
from outlinecompilation import serializers


# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
