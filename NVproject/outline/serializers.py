from rest_framework import serializers
from outline.models import User, DeCuongMonHoc, MucTieuMonHoc, ChuanDauRaCTDT, KeHoachGiangDay, Diem, MonHoc, GiangVien, \
    SinhVien


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'email', 'avatar']
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        print(data)
        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class StudentSerializer(serializers.Serializer):
    class Meta:
        model = SinhVien
        fields = UserSerializer.Meta.fields + ["nganh", ]


class LecturerSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiangVien
        fields = UserSerializer.Meta.fields + ["khoa", "title", "degree"]


class TeachingPlanSerializer(serializers.Serializer):
    class Meta:
        model = KeHoachGiangDay
        fields = ["ty_trong", "hinh_thuc_danh_gia", "phan_loai"]


class ScoreSerilizer(serializers.Serializer):
    class Meta:
        model = Diem
        fields = '__all__'


class ProgrammeLearningOutcomeSerializer(serializers.ModelSerializer):
    class Meta:
        model = ChuanDauRaCTDT
        fields = '__all__'


class CourseObjectiveSerializer(serializers.ModelSerializer):
    class Meta:
        model = MucTieuMonHoc
        fields = ['stt', 'mo_ta']


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonHoc
        fields = ['ten_mon_hoc', 'ten_mon_hoc_ta', 'thuoc_khoi_kien_thuc',
                  'so_tin_chi_thuc_hanh', 'so_tin_chi_ly_thuyet', 'so_tin_chi_tu_hoc',
                  'mo_ta_mon_hoc', 'mon_tien_quyet', 'mon_hoc_truoc', 'mon_song_hanh']


class OutlineSerializer(serializers.ModelSerializer):
    mon_hoc = SubjectSerializer()
    giang_vien_bien_soan = LecturerSerializer()
    co = serializers.SerializerMethodField()
    s = serializers.SerializerMethodField()
    tp = serializers.SerializerMethodField()
    r = serializers.SerializerMethodField()

    def get_co(self, outline):
        datas = outline.muctieumonhoc_set.all()
        return [{"stt": data.stt, "mo_ta": data.mo_ta} for data in datas]

    def get_s(self, outline):
        datas = outline.diem_set.all()
        return [{"ty_trong": data.ty_trong, "hinh_thuc_danh_gia": data.hinh_thuc_danh_gia, "phan_loai": data.phan_loai} for data in datas]

    def get_tp(self, outline):
        datas = outline.kehoachgiangday_set.all()
        return [{"tuan": data.tuan, "noi_dung_chuong": data.noi_dung_chuong} for data in datas]

    def get_r(self, outline):
        return outline.hoclieu_set.all().values()

    class Meta:
        model = DeCuongMonHoc
        fields = ['giang_vien_bien_soan', 'mon_hoc', 'created_date', 'co',
                  'r', 'phuong_phap_giang_day_hoc_tap', 's', 'tp']
