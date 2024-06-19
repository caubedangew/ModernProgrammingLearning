from rest_framework import serializers
from outline.models import User, DeCuongMonHoc, MonHoc, GiangVien, SinhVien, Comment, HocLieu, Khoa, Nganh, \
    MucTieuMonHoc, ChuanDauRaMonHoc, Diem, KeHoachGiangDay, HoatDongDayVaHoc, HocLieu_DeCuongMonHoc, MucDoDapUng, \
    Chuong, ChuanDauRaCTDT


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['avatar'] = instance.avatar.url
        return req


class UserSerializer(ItemSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', 'avatar', 'sex', 'date_of_birth', 'address', 'user_role']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }


class FieldSerializer(serializers.ModelSerializer):
    class Meta:
        model = Nganh
        fields = ["ten_nganh"]


class StudentSerializer(serializers.ModelSerializer):
    nganh = FieldSerializer()

    class Meta:
        model = SinhVien
        fields = ['id', 'first_name', 'last_name', 'nganh', "email", "avatar"]


class StudentDetailSerializer(ItemSerializer):
    class Meta:
        model = StudentSerializer.Meta.model
        fields = StudentSerializer.Meta.fields + ["sex", "date_of_birth", 'address']


class FacultySerializer(serializers.ModelSerializer):
    class Meta:
        model = Khoa
        fields = ["ten_khoa"]


class LecturerSerializer(serializers.ModelSerializer):
    khoa = FacultySerializer()

    class Meta:
        model = GiangVien
        fields = ["id", "first_name", "last_name", "email", "khoa", 'avatar']


class LecturerDetailSerializer(ItemSerializer):
    class Meta:
        model = LecturerSerializer.Meta.model
        fields = LecturerSerializer.Meta.fields + ["sex", "date_of_birth", 'address', 'title', 'degree']


class SubjectSerializer(serializers.ModelSerializer):
    mon_tien_quyet = serializers.SerializerMethodField()
    mon_hoc_truoc = serializers.SerializerMethodField()
    mon_song_hanh = serializers.SerializerMethodField()
    so_tin_chi = serializers.SerializerMethodField()

    def get_mon_tien_quyet(self, subject):
        return [{"ten_mon_hoc": data.ten_mon_hoc} for data in subject.mon_tien_quyet.all()]

    def get_mon_hoc_truoc(self, subject):
        return [{"ten_mon_hoc": data.ten_mon_hoc} for data in subject.mon_hoc_truoc.all()]

    def get_mon_song_hanh(self, subject):
        return [{"ten_mon_hoc": data.ten_mon_hoc} for data in subject.mon_song_hanh.all()]

    def get_so_tin_chi(self, obj):
        return obj.so_tin_chi_thuc_hanh + obj.so_tin_chi_ly_thuyet

    class Meta:
        model = MonHoc
        fields = ['id', 'ten_mon_hoc', 'ten_mon_hoc_ta', 'so_tin_chi', 'ThuocKhoiKienThuc', 'mo_ta_mon_hoc',
                  'so_tin_chi_thuc_hanh', 'so_tin_chi_ly_thuyet', 'mon_tien_quyet', 'mon_hoc_truoc', 'mon_song_hanh']


class ChapterSerializer(serializers.ModelSerializer):
    class Meta:
        model = Chuong
        fields = ["so_thu_tu_chuong", "ten_chuong"]


class CourseObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MucTieuMonHoc
        fields = ["stt", "mo_ta"]


class ScoreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Diem
        fields = ["ty_trong", "hinh_thuc_danh_gia", "phan_loai"]


class ReferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HocLieu
        fields = ['ten_hoc_lieu']


class Reference_OutlineSerializer(serializers.ModelSerializer):
    hoc_lieu = ReferencesSerializer()
    class Meta:
        model = HocLieu_DeCuongMonHoc
        fields = ["stt", "hoc_lieu"]


class ResponsiveLevel(serializers.ModelSerializer):
    class Meta:
        model = MucDoDapUng
        fields = ["chuan_dau_ra_ctdt", "muc_do_dap_ung"]


class CourseLearningOutcomeSerializer(serializers.ModelSerializer):
    muc_tieu_mon_hoc = CourseObjectiveSerializer()
    dap_ung = serializers.SerializerMethodField()

    def get_dap_ung(self, clo):
        return ResponsiveLevel(clo.mucdodapung_set.all(), many=True).data

    class Meta:
        model = ChuanDauRaMonHoc
        fields = ["muc_tieu_mon_hoc", "stt", "mo_ta", "dap_ung"]


class TeachingAndStudyingActivitySerializer(serializers.ModelSerializer):
    class Meta:
        model = HoatDongDayVaHoc
        fields = ["so_tiet", "cong_viec", "loai_hoat_dong"]


class TeachingPlanSerializer(serializers.ModelSerializer):
    chuong = ChapterSerializer()
    hoat_dong_day_va_hoc = serializers.SerializerMethodField()
    hoc_lieu = serializers.SerializerMethodField()
    bai_danh_gia = ScoreSerializer(many=True)
    chuan_dau_ra_mon_hoc = CourseLearningOutcomeSerializer(many=True)

    def get_hoc_lieu(self, teaching_plan):
        hoc_lieu = []
        for r in teaching_plan.hoc_lieu.all():
            hoc_lieu.append(Reference_OutlineSerializer(r.hoclieu_decuongmonhoc_set.all(), many=True).data)
        return hoc_lieu

    def get_hoat_dong_day_va_hoc(self, teaching_plan):
        return TeachingAndStudyingActivitySerializer(teaching_plan.hoatdongdayvahoc_set.all(), many=True).data

    class Meta:
        model = KeHoachGiangDay
        fields = ["tuan", "chuong", "noi_dung_chuong", "hoat_dong_day_va_hoc", "hoc_lieu", "bai_danh_gia", "chuan_dau_ra_mon_hoc"]


class OutlineSerializer(serializers.ModelSerializer):
    mon_hoc = SubjectSerializer()
    giang_vien_bien_soan = LecturerSerializer()

    # def create(self, validated_data):
    #     data = validated_data.copy()
    #     tong = sum(float(s) for s in data["s"]["ty_trong"])
    #     if tong != 1.0:
    #         raise ValidationError("Tỷ trọng điểm chưa đủ 100%")
    #     return DeCuongMonHoc.objects.create(**data)

    class Meta:
        model = DeCuongMonHoc
        fields = ['id', 'giang_vien_bien_soan', 'mon_hoc', 'created_date']


class OutlineDetailSerializer(serializers.ModelSerializer):
    mon_hoc = SubjectSerializer()
    giang_vien_bien_soan = LecturerSerializer()
    co = serializers.SerializerMethodField()
    clo = serializers.SerializerMethodField()
    r = serializers.SerializerMethodField()
    s = serializers.SerializerMethodField()
    tp = serializers.SerializerMethodField()

    def get_co(self, outline):
        return CourseObjectiveSerializer(outline.muctieumonhoc_set.all(), many=True).data

    def get_r(self, outline):
        return Reference_OutlineSerializer(outline.hoclieu_decuongmonhoc_set.all(), many=True).data

    def get_clo(self, outline):
        return [CourseLearningOutcomeSerializer(data.chuandauramonhoc_set.all(), many=True).data for data in outline.muctieumonhoc_set.all()]

    def get_s(self, outline):
        return ScoreSerializer(outline.diem_set.all(), many=True).data

    def get_tp(self, outline):
        return TeachingPlanSerializer(outline.kehoachgiangday_set.all(), many=True).data

    class Meta:
        model = DeCuongMonHoc
        fields = (OutlineSerializer.Meta.fields +
                  ['co', 'clo', 'r', 'phuong_phap_giang_day_hoc_tap', 's', 'tp', 'quy_dinh'])


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ["content", "user", "created_date"]


class ProgrammeLearningOutcomeSerializer:
    class Meta:
        model = ChuanDauRaCTDT
        fields = ['stt', 'mo_ta', 'loaicdrctdt']