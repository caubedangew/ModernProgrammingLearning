from django.contrib import admin
from rest_framework import routers
from django.urls import path, include
from outlinecompilation import views

r = routers.DefaultRouter()
r.register('users', views.UserViewSet)

urlpatterns = [
    path('', include(r.urls)),
]