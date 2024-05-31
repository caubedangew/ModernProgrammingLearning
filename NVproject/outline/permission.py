from rest_framework import permissions

from outline.models import GiangVien


class LecturerOwnerAuthorization(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, outline):
        return super().has_permission(request, view) and request.user == outline.giang_vien_bien_soan


class LecturerAuthorization(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return GiangVien.objects.filter(pk=request.user.id).exists()
