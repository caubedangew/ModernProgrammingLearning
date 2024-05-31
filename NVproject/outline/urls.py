from django.urls import path, include
from rest_framework import routers
from outline import views

r = routers.DefaultRouter()
r.register('users', views.UserViewSet, 'users')
r.register('outlines', views.OutlineViewSet, 'outlines')
r.register('outlines', views.OutlineDetailViewSet, 'outlineDetails')
r.register('lecturers', views.LecturerViewSet, 'lecturers')
r.register('students', views.StudentViewSet, 'students')

urlpatterns = [
    path('', include(r.urls)),
]
