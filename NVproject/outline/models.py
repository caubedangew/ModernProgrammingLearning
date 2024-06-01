from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import AbstractUser
from django.db import models
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField


# Create your models here.
class User(AbstractUser):
    class VaiTro(models.IntegerChoices):
        SinhVien = 1
        GiangVien = 2

        def __str__(self):
            return self.name

    username = models.CharField(max_length=20, null=True, unique=True)
    password = models.CharField(max_length=255, null=True)
    user_role = models.IntegerField(VaiTro)
    avatar = CloudinaryField()
    sex = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True)

    def get_full_name(self):
        full_name = "%s %s" % (self.last_name, self.first_name)
        return full_name.strip()

    def __str__(self):
        return self.get_full_name()

    def save(self, *args, **kwargs):
        if self.password and not self.password.startswith('pbkdf2_sha256$'):
            self.password = make_password(self.password)

        super().save(*args, **kwargs)


class GiangVien(User):
    title = models.CharField(max_length=100, null=True)
    degree = models.CharField(max_length=30, null=True)
    khoa = models.ForeignKey('Khoa', on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = "Giang vien"


class SinhVien(User):
    nganh = models.ForeignKey('Nganh', on_delete=models.PROTECT, null=True)

    class Meta:
        verbose_name = "Sinh vien"


class BaseModel(models.Model):
    active = models.BooleanField(default=True)
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Khoa(BaseModel):
    ten_khoa = models.CharField(max_length=50)

    def __str__(self):
        return self.ten_khoa


class Nganh(BaseModel):
    ten_nganh = models.CharField(max_length=50)
    khoa = models.ForeignKey(Khoa, on_delete=models.RESTRICT)
    loaiCDRCTDT = models.ManyToManyField('LoaiCDRCTDT')

    def __str__(self):
        return self.ten_nganh


class MonHoc(BaseModel):
    ten_mon_hoc = models.CharField(max_length=100)
    ten_mon_hoc_ta = models.CharField(max_length=100)
    thuoc_khoi_kien_thuc = models.CharField(max_length=50)
    so_tin_chi = models.FloatField(default=0)
    so_tin_chi_thuc_hanh = models.FloatField(default=0)
    so_tin_chi_ly_thuyet = models.FloatField(default=0)
    so_tin_chi_tu_hoc = models.FloatField(default=0)
    mo_ta_mon_hoc = RichTextField()
    mon_tien_quyet = models.ManyToManyField('MonHoc', blank=True, related_name='mtq')
    mon_hoc_truoc = models.ManyToManyField('MonHoc', blank=True, related_name='mht')
    mon_song_hanh = models.ManyToManyField('MonHoc', blank=True, related_name='msh')
    nganh = models.ManyToManyField(Nganh)

    def __str__(self):
        return self.ten_mon_hoc


class Chuong(BaseModel):
    so_thu_tu_chuong = models.IntegerField(default=0)
    ten_chuong = models.CharField(max_length=100)
    mon_hoc = models.ForeignKey(MonHoc, on_delete=models.CASCADE)

    def __str__(self):
        return "Chương %s - %s - %s" % (self.so_thu_tu_chuong.__str__(), self.ten_chuong.__str__(), self.mon_hoc.__str__())


class DeCuongMonHoc(BaseModel):
    phuong_phap_giang_day_hoc_tap = RichTextField()
    giang_vien_bien_soan = models.ForeignKey(GiangVien, on_delete=models.PROTECT)
    mon_hoc = models.ForeignKey(MonHoc, on_delete=models.RESTRICT)
    hoc_lieu = models.ManyToManyField('HocLieu')

    def __str__(self):
        return self.mon_hoc.__str__() + " - " + self.giang_vien_bien_soan.__str__() + " - " + self.created_date.year.__str__()


class KeHoachGiangDay(BaseModel):
    tuan = models.IntegerField(default=0)
    noi_dung_chuong = RichTextField()
    de_cuong_mon_hoc = models.ForeignKey(DeCuongMonHoc, on_delete=models.CASCADE)
    chuong = models.ForeignKey(Chuong, on_delete=models.CASCADE)
    hoc_lieu = models.ManyToManyField('HocLieu')

    def __str__(self):
        return "Tuần %s - %s - %s" % (self.tuan.__str__(), self.chuong.__str__(), self.de_cuong_mon_hoc.__str__())


class HoatDongDayVaHoc(BaseModel):
    so_tiet = models.FloatField(default=0)
    cong_viec = RichTextField()
    loai_hoat_dong = models.CharField(max_length=30)
    ke_hoach_giang_day = models.ForeignKey(KeHoachGiangDay, on_delete=models.CASCADE)

    def __str__(self):
        return self.loaiHoatDong.__str__() + " - " + self.ke_hoach_giang_day.__str__()


class LoaiCDRCTDT(BaseModel):
    stt = models.IntegerField(default=0)
    ten_loai = models.CharField(max_length=255)

    def __str__(self):
        return self.ten_loai


class MoTaModel(BaseModel):
    stt = models.IntegerField(default=0)
    mo_ta = RichTextField()

    class Meta:
        abstract = True


class ChuanDauRaCTDT(MoTaModel):
    loaicdrctdt = models.ForeignKey(LoaiCDRCTDT, on_delete=models.PROTECT)
    nganh = models.ForeignKey(Nganh, on_delete=models.PROTECT)

    def __str__(self):
        return self.stt.__str__() + " - " + self.nganh.__str__()


class MucTieuMonHoc(MoTaModel):
    de_cuong_mon_hoc = models.ForeignKey(DeCuongMonHoc, on_delete=models.CASCADE)
    chuan_dau_ra_ctdt = models.ManyToManyField(ChuanDauRaCTDT)

    def __str__(self):
        return self.stt.__str__() + " - " + self.de_cuong_mon_hoc.__str__()


class ChuanDauRaMonHoc(MoTaModel):
    muc_tieu_mon_hoc = models.ForeignKey(MucTieuMonHoc, on_delete=models.CASCADE)
    diem = models.ManyToManyField('Diem')

    def __str__(self):
        return "CO" + self.stt.__str__() + " - " + self.muc_tieu_mon_hoc.__str__()


class HocLieu(BaseModel):
    ten_hoc_lieu = models.CharField(max_length=500)

    def __str__(self):
        return self.ten_hoc_lieu


class Diem(BaseModel):
    class PhanLoaiDiem(models.TextChoices):
        QuaTrinh = 'QT'
        GiuaKy = 'GK'
        CuoiKy = 'CK'

        def __str__(self):
            return self.name
    ty_trong = models.FloatField(default=0)
    hinh_thuc_danh_gia = models.CharField(max_length=50)
    de_cuong_mon_hoc = models.ForeignKey(DeCuongMonHoc, on_delete=models.CASCADE)
    phan_loai = models.CharField(max_length=2, choices=PhanLoaiDiem.choices)

    def __str__(self):
        return self.phan_loai.__str__() + " - " + self.hinh_thuc_danh_gia.__str__() + " - " + self.de_cuong_mon_hoc.__str__()


class Comment(BaseModel):
    content = RichTextField(max_length=255)
    outline = models.ForeignKey(DeCuongMonHoc, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
