from rest_framework import permissions

from outline.models import GiangVien


class LecturerOwnerAuthorization(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, outline):
        return super().has_permission(request, view) and (outline.giang_vien_bien_soan.email == request.user.email)


class LecturerAuthorization(permissions.IsAuthenticated):
    def has_permission(self, request, view):
        return GiangVien.objects.filter(pk=request.user.id).exists()


class CommentOwnerAuthorization(permissions.IsAuthenticated):
    def has_object_permission(self, request, view, obj):
        return super().has_permission(request, view) and obj.user == request.user
