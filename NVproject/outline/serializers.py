from rest_framework import serializers
from outline.models import User, DeCuongMonHoc, MucTieuMonHoc, ChuanDauRaCTDT, KeHoachGiangDay, Diem, MonHoc, GiangVien


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


class LectureSerializer(serializers.ModelSerializer):
    class Meta:
        model = GiangVien
        fields = UserSerializer.Meta.fields


class StudyingPlanSerializer(serializers.Serializer):
    class Meta:
        model = KeHoachGiangDay
        fields = '__all__'


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
        fields = '__all__'


class SubjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = MonHoc
        fields = ['ten_mon_hoc', 'ten_mon_hoc_ta', 'thuoc_khoi_kien_thuc',
                  'so_tin_chi_thuc_hanh', 'so_tin_chi_ly_thuyet', 'so_tin_chi_tu_hoc',
                  'mo_ta_mon_hoc', 'mon_tien_quyet', 'mon_hoc_truoc', 'mon_song_hanh']


class OutlineSerializer(serializers.ModelSerializer):
    mon_hoc = SubjectSerializer()
    giang_vien_bien_soan = LectureSerializer()
    co = serializers.SerializerMethodField()
    s = serializers.SerializerMethodField()
    tp = serializers.SerializerMethodField()
    r = serializers.SerializerMethodField()

    def get_co(self, outline):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return outline.muctieumonhoc_set.all().values()

    def get_s(self, outline):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return outline.diem_set.all().values()

    def get_tp(self, outline):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return outline.kehoachgiangday_set.all().values()

    def get_r(self, outline):
        request = self.context.get('request')
        if request.user.is_authenticated:
            return outline.hoclieu_set.all().values()

    class Meta:
        model = DeCuongMonHoc
        fields = ['giang_vien_bien_soan', 'mon_hoc', 'created_date', 'co',
                  'r', 'phuong_phap_giang_day_hoc_tap', 's', 'tp']
