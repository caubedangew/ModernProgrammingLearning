from django.shortcuts import render
from rest_framework import viewsets, generics, status, permissions
from rest_framework.decorators import action
from rest_framework.response import Response

from outline import serializers, paginators
from outline.models import User, DeCuongMonHoc, GiangVien


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
    queryset = DeCuongMonHoc.objects.prefetch_related('muctieumonhoc_set').all()
    serializer_class = serializers.OutlineSerializer
    # permission_classes = [permissions.IsAuthenticated]

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


