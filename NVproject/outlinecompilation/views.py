from django.shortcuts import render
from rest_framework import viewsets, generics, status
from outlinecompilation.models import User
from outlinecompilation import serializers
from rest_framework.decorators import action
from rest_framework.response import Response


# Create your views here.
class UserViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer

    @action(methods=['post'], url_path='register', detail=False)
    def register(self, request):
        user = self.get_object().create()
        for k, v in request.data.items():
            setattr(user, k, v)
        user.save()
        return Response(serializers.UserSerializer(user).data, status=status.HTTP_201_CREATED)

