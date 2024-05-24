from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from outline import serializers, paginators, permissions
from outline.models import User, DeCuongMonHoc, GiangVien, SinhVien


# Create your views here.


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer

    def get_permissions(self):
        if self.action in ['current_user']:
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get', 'patch'], url_path='current-user', detail=False)
    def current_user(self, request):
        user = request.user
        if request.method.__eq__("PATCH"):
            for k, v in request.data.items():
                setattr(user, k, v)
            user.save()

        return Response(serializers.UserSerializer(user).data)


class OutlineViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = DeCuongMonHoc.objects.all()
    serializer_class = serializers.OutlineSerializer
    # permission_classes = [permissions.IsAuthenticated]

    def get_permissions(self):
        if self.action in ["edit_outline"]:
            return [permissions.LectureOwnerAuthentication()]
        return [permissions.AllowAny()]

    @action(methods=['post'], url_path='compile', detail=False)
    def compile_outline(self, request):
        giang_vien_bien_soan = GiangVien.objects.filter(pk=request.user.id).first()
        if giang_vien_bien_soan:
            outline = DeCuongMonHoc.objects.create(giang_vien_bien_soan=giang_vien_bien_soan,
                                                   mon_hoc_id=request.data.get("mon_hoc"),
                                                   phuong_phap_giang_day_hoc_tap=
                                                   request.data.get("phuong_phap_giang_day_hoc_tap"))
            return Response(serializers.OutlineSerializer(outline).data, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_403_FORBIDDEN)

    @action(methods=["patch"], detail=True, url_path="edit")
    def edit_outline(self, pk, request):
        outline = DeCuongMonHoc.objects.filter(pk=pk)
        if outline:
            for k, v in request.data.items():
                setattr(outline, k, v)
            return Response(serializers.OutlineSerializer(outline).data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class LecturerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = GiangVien.objects.filter(is_active=True).all()
    serializer_class = serializers.LecturerSerializer


class StudentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = SinhVien.objects.filter(is_active=True).all()
    serializer_class = serializers.StudentSerializer
