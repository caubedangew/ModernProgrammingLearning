from rest_framework.permissions import BasePermission


class LectureOwnerAuthentication(BasePermission):
    def has_object_permission(self, request, view, obj):
        return self.has_permission(request, view) and obj.giang_vien_bien_soan == request.user