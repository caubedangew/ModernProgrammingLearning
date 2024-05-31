from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from outline.models import User, DeCuongMonHoc, MucTieuMonHoc, ChuanDauRaCTDT, KeHoachGiangDay, Diem, MonHoc, GiangVien, \
    SinhVien, Comment, HocLieu


class ItemSerializer(serializers.ModelSerializer):
    def to_representation(self, instance):
        req = super().to_representation(instance)
        req['avatar'] = instance.avatar.url
        return req


class UserSerializer(ItemSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name', 'last_name', 'email', ]
        extra_kwargs = {
            'password': {
                'write_only': True
            }
        }

    def create(self, validated_data):
        data = validated_data.copy()
        user = User(**data)
        user.set_password(data['password'])
        user.save()

        return user


class StudentSerializer(ItemSerializer):
    class Meta:
        model = SinhVien
        fields = UserSerializer.Meta.fields + ["nganh", ]


class StudentDetailSerializer(ItemSerializer):
    class Meta:
        model = StudentSerializer.Meta.model
        fields = StudentSerializer.Meta.fields + ["avatar"]


class LecturerSerializer(ItemSerializer):
    class Meta:
        model = GiangVien
        fields = UserSerializer.Meta.fields + ["khoa"]


class LecturerDetailSerializer(LecturerSerializer):
    class Meta:
        model = LecturerSerializer.Meta.model
        fields = LecturerSerializer.Meta.fields + ['avatar', 'title', 'degree']


class SubjectSerializer(serializers.ModelSerializer):
    so_tin_chi = serializers.SerializerMethodField()

    def get_so_tin_chi(self, obj):
        return obj.so_tin_chi_thuc_hanh + obj.so_tin_chi_ly_thuyet

    class Meta:
        model = MonHoc
        fields = ['ten_mon_hoc', 'ten_mon_hoc_ta', 'so_tin_chi',
                  'so_tin_chi_thuc_hanh', 'so_tin_chi_ly_thuyet']


class ReferencesSerializer(serializers.ModelSerializer):
    class Meta:
        model = HocLieu
        fields = ['ten_hoc_lieu']


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
    s = serializers.SerializerMethodField()
    tp = serializers.SerializerMethodField()
    hoc_lieu = ReferencesSerializer(many=True)

    def get_co(self, outline):
        datas = outline.muctieumonhoc_set.all()
        return [{"stt": data.stt, "mo_ta": data.mo_ta} for data in datas]

    def get_s(self, outline):
        datas = outline.diem_set.all()
        return [{"ty_trong": data.ty_trong, "hinh_thuc_danh_gia": data.hinh_thuc_danh_gia, "phan_loai": data.phan_loai}
                for data in datas]

    def get_tp(self, outline):
        datas = outline.kehoachgiangday_set.all()
        return [{"tuan": data.tuan, "noi_dung_chuong": data.noi_dung_chuong} for data in datas]

    class Meta:
        model = DeCuongMonHoc
        fields = (OutlineSerializer.Meta.fields +
                  ['co', 'hoc_lieu', 'phuong_phap_giang_day_hoc_tap', 's', 'tp'])


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ["content", "user", "created_date"]
