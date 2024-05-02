from django.urls import path, include
from rest_framework import routers
from outline import views

r = routers.DefaultRouter()
r.register('users', views.UserViewSet, 'users')
r.register('outlines', views.OutlineViewSet, 'outlines')

urlpatterns = [
    path('', include(r.urls)),
]
