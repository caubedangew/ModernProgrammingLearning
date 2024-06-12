from rest_framework import serializers
from outline.models import User, DeCuongMonHoc, MonHoc, GiangVien, SinhVien, Comment, HocLieu


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
        fields = ['id', 'ten_mon_hoc', 'ten_mon_hoc_ta', 'so_tin_chi',
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
    clo = serializers.SerializerMethodField()
    s = serializers.SerializerMethodField()
    tp = serializers.SerializerMethodField()
    hoc_lieu = ReferencesSerializer(many=True)

    def get_co(self, outline):
        datas = outline.muctieumonhoc_set.all()
        return [{"stt": data.stt, "mo_ta": data.mo_ta} for data in datas]

    def get_clo(self, outline):
        var = []
        for data in outline.muctieumonhoc_set.all():
            for d in data.chuandauramonhoc_set.all():
                var.append([{"clo": d.__str__(), "dap_ung":
                    [{"plo": da.chuan_dau_ra_ctdt.__str__(), "muc_do_dap_ung": da.muc_do_dap_ung}
                     for da in d.mucdodapung_set.all()]
                             }])
        return var

    def get_s(self, outline):
        datas = outline.diem_set.all()
        return [{"ty_trong": data.ty_trong, "hinh_thuc_danh_gia": data.hinh_thuc_danh_gia, "phan_loai": data.phan_loai}
                for data in datas]

    def get_tp(self, outline):
        datas = outline.kehoachgiangday_set.all()
        return [{"tuan": data.tuan, "noi_dung_chuong": data.noi_dung_chuong,
                 "chuong": data.chuong.__str__().strip("-")[7:9],
                 "chuan_dau_ra_mon_hoc": [d.__str__() for d in data.chuan_dau_ra_mon_hoc.all()],
                 "hoc_lieu": [d.__str__() for d in data.hoc_lieu.all()],
                 "hoat_dong_day_va_hoc": [
                     {"so_tiet": d.so_tiet, "cong_viec": d.cong_viec, "loai_hoat_dong": d.loai_hoat_dong}
                     for d in data.hoatdongdayvahoc_set.all()]} for data in datas]

    class Meta:
        model = DeCuongMonHoc
        fields = (OutlineSerializer.Meta.fields +
                  ['co', 'clo', 'hoc_lieu', 'phuong_phap_giang_day_hoc_tap', 's', 'tp', 'quy_dinh'])


class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = Comment
        fields = ["content", "user", "created_date"]
