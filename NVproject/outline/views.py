from rest_framework import viewsets, generics, status, permissions, parsers
from rest_framework.decorators import action
from rest_framework.response import Response

from outline import serializers, paginators, permission
from outline.models import User, DeCuongMonHoc, GiangVien, SinhVien, Comment, MucTieuMonHoc, Diem, KeHoachGiangDay, \
    ChuanDauRaMonHoc, HocLieu, Chuong, ChuanDauRaCTDT
from outline.serializers import StudentDetailSerializer


# Create your views here.


class UserViewSet(viewsets.ViewSet, generics.CreateAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = serializers.UserSerializer
    parser_classes = [parsers.MultiPartParser, ]

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
    queryset = DeCuongMonHoc.objects.order_by("created_date", "-created_date")
    serializer_class = serializers.OutlineSerializer
    permission_classes = [permissions.IsAuthenticated()]
    parser_classes = [parsers.JSONParser]

    def get_queryset(self):
        queryset = self.queryset
        outline_name = self.request.query_params.get("oName")
        if outline_name:
            queryset = queryset.filter(mon_hoc__ten_mon_hoc__icontains=outline_name)

        credit_numbers = self.request.query_params.get("number")
        if credit_numbers:
            queryset = queryset.filter(mon_hoc__so_tin_chi=float(credit_numbers))

        lecturer_name = self.request.query_params.get("lName")
        if lecturer_name:
            queryset = queryset.filter(giang_vien_bien_soan__first_name__icontains=lecturer_name)

        return queryset

    def get_permissions(self):
        if self.action in ["edit_outline"]:
            return [permission.LecturerOwnerAuthorization()]
        elif self.action in ["compile_outline"]:
            return [permission.LecturerAuthorization()]
        return self.permission_classes

    @action(methods=['get'], url_path="comments", detail=True)
    def get_comments(self, request, pk):
        comments = self.get_object().comment_set.select_related('user').all()

        paginator = paginators.CommentPaginator()
        page = paginator.paginate_queryset(comments, request)
        if page is not None:
            serializer = serializers.CommentSerializer(page, many=True)
            return paginator.get_paginated_response(serializer.data)

        return Response(serializers.CommentSerializer(comments, many=True).data)

    @action(methods=["post"], url_path='comments', detail=True)
    def add_comment(self, request, pk):
        outline = self.get_object().comment_set.create(user=request.user, content=request.data.get("content"))

        return Response(serializers.CommentSerializer(outline).data, status=status.HTTP_201_CREATED)

    @action(methods=['post'], url_path='compile', detail=False)
    def compile_outline(self, request):
        data = request.data
        outline = self.get_object().create(giang_vien_bien_soan=request.user,
                                           mon_hoc=data.get("mon_hoc"),
                                           phuong_phap_giang_day_hoc_tap=
                                           data.get("phuong_phap_giang_day_hoc_tap"))
        for co in data.get("co"):
            muc_tieu_mon_hoc = MucTieuMonHoc.objects.create(stt=co.stt, mo_ta=co.mo_ta, de_cuong_mon_hoc=outline)
            for clo in data.get("clo"):
                muc_tieu_mon_hoc.chuandauramonhoc_set.create(stt=clo.stt, mo_ta=clo.mo_ta)
        for hoc_lieu in data.get("hoc_lieu"):
            self.get_object().hoclieu_set.create(stt=hoc_lieu.stt, ten_hoc_lieu=hoc_lieu.ten_hoc_lieu)
        for s in data.get("s"):
            Diem.objects.create(ty_trong=s.ty_trong, hinh_thuc_danh_gia=s.hinh_thuc_danh_gia, phan_loai=s.phan_loai)
        for tp in data.get("tp"):
            teaching_plan = KeHoachGiangDay.objects.create(tuan=tp.tuan, noi_dung_chuong=tp.noi_dung_chuong, de_cuong_mon_hoc=outline,
                                           chuong_id=tp.chuong)
            teaching_plan.hoc_lieu.get_or_create(stt=tp.stt, hoc_lieu__ten_hoc_lieu=tp.ten_hoc_lieu)
            teaching_plan.chuan_dau_ra_mon_hoc.get_or_create()


        return Response(serializers.OutlineSerializer(outline).data, status=status.HTTP_201_CREATED)

    @action(methods=["patch"], detail=True, url_path="edit")
    def edit_outline(self, request, pk):
        outline = self.get_object().get(pk=pk)
        if outline:
            for k, v in request.data.items():
                setattr(outline, k, v)
            return Response(serializers.OutlineSerializer(outline).data)
        return Response(status=status.HTTP_404_NOT_FOUND)


class OutlineDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = DeCuongMonHoc.objects.filter(active=True)
    serializer_class = serializers.OutlineDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class LecturerViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = GiangVien.objects.filter(is_active=True).all()
    serializer_class = serializers.LecturerSerializer


class LecturerDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = LecturerViewSet.queryset
    serializer_class = serializers.LecturerDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = SinhVien.objects.filter(is_active=True)
    serializer_class = serializers.StudentSerializer
    permission_classes = [permissions.IsAuthenticated]


class StudentDetailViewSet(viewsets.ViewSet, generics.RetrieveAPIView):
    queryset = StudentViewSet.queryset
    serializer_class = StudentDetailSerializer
    permission_classes = [permissions.IsAuthenticated]


class CommentViewSet(viewsets.ViewSet, generics.UpdateAPIView, generics.DestroyAPIView):
    queryset = Comment.objects.filter(active=True)
    serializer_class = serializers.CommentSerializer
    permission_classes = [permission.CommentOwnerAuthorization]


class ReferencesViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = HocLieu.objects.filter(active=True)
    serializer_class = serializers.ReferencesSerializer
    permission_classes = [permission.LecturerAuthorization]


class ChapterViewSet(viewsets.ViewSet, generics.ListCreateAPIView):
    queryset = Chuong.objects.filter(active=True)
    serializer_class = serializers.ChapterSerializer
    permission_classes = [permission.LecturerAuthorization]


class ProgrammeLearningOutcomeViewSet(viewsets.ViewSet, generics.ListAPIView):
    queryset = ChuanDauRaCTDT.objects.filter(active=True)
    serializer_class = serializers.ProgrammeLearningOutcomeSerializer
    permission_classes = [permission.LecturerAuthorization]


