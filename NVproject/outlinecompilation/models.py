from django.db import models
from django.contrib.auth.models import AbstractUser
from ckeditor.fields import RichTextField
from cloudinary.models import CloudinaryField
from datetime import date


class User(AbstractUser):
    class VaiTro(models.IntegerChoices):
        SinhVien = 1
        GiangVien = 2
    user_role = models.IntegerField(VaiTro, default=1)
    avatar = CloudinaryField(null=True)
    sex = models.BooleanField(default=True)
    date_of_birth = models.DateField(null=True)
    address = models.CharField(max_length=255, null=True)

    def __str__(self):
        return self.first_name + " " + self.last_name


class GiangVien(User):
    title = models.CharField(max_length=100)
    degree = models.CharField(max_length=30)
    khoa = models.ForeignKey('Khoa', on_delete=models.PROTECT)

    class Meta:
        verbose_name = "Giang vien"


class SinhVien(User):
    nganh = models.ForeignKey('Nganh', on_delete=models.PROTECT)

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

    def __str__(self):
        return self.ten_nganh


class MonHoc(BaseModel):
    ten_mon_hoc = models.CharField(max_length=100)
    # ten_mon_hoc_ta = models.CharField(max_length=100)
    so_tin_chi_thuc_hanh = models.FloatField(default=0)
    so_tin_chi_ly_thuyet = models.FloatField(default=0)
    so_tin_chi_tu_hoc = models.FloatField(default=0)
    mo_ta_mon_hoc = RichTextField()
    mon_tien_quyet = models.ManyToManyField('MonHoc', null=True, blank=True, related_name='mtq')
    mon_hoc_truoc = models.ManyToManyField('MonHoc', null=True, blank=True, related_name='mht')
    mon_song_hanh = models.ManyToManyField('MonHoc', null=True, blank=True, related_name='msh')
    nganh = models.ManyToManyField(Nganh)

    def __str__(self):
        return self.ten_mon_hoc


class Chuong(BaseModel):
    so_thu_tu_chuong = models.IntegerField(default=0)
    ten_chuong = models.CharField(max_length=100)
    mon_hoc = models.ForeignKey(MonHoc, on_delete=models.CASCADE)

    def __str__(self):
        return self.ten_chuong.__str__() + " - " + self.mon_hoc.__str__()


class DeCuongMonHoc(BaseModel):
    phuong_phap_giang_day_hoc_tap = RichTextField()
    giang_vien_bien_soan = models.ForeignKey(GiangVien, on_delete=models.PROTECT)
    mon_hoc = models.ForeignKey(MonHoc, on_delete=models.RESTRICT)
    nam_bien_soan = models.IntegerField(default=date.today().strftime("%Y"))

    def __str__(self):
        return self.mon_hoc.__str__() + " - " + self.giang_vien_bien_soan.__str__() + " - " + self.nam_bien_soan.__str__()


class KeHoachGiangDay(BaseModel):
    tuan = models.IntegerField(default=0)
    noi_dung_chuong = models.CharField(max_length=1000)
    de_cuong_mon_hoc = models.ForeignKey(DeCuongMonHoc, on_delete=models.CASCADE)
    chuong = models.ForeignKey(Chuong, on_delete=models.CASCADE)

    def __str__(self):
        return self.tuan.__str__() + " - " + self.chuong.__str__() + " - " + self.de_cuong_mon_hoc.__str__()


class HoatDongDayVaHoc(BaseModel):
    so_tiet = models.FloatField(default=0)
    congViec = RichTextField()
    loaiHoatDong = models.CharField(max_length=30)
    ke_hoach_giang_day = models.ForeignKey(KeHoachGiangDay, on_delete=models.CASCADE)

    def __str__(self):
        return self.loaiHoatDong.__str__() + " - " + self.ke_hoach_giang_day.__str__()


class LoaiCDRCTDT(BaseModel):
    stt = models.IntegerField(default=0)
    ten_loai = models.CharField(max_length=255)
    nganh = models.ManyToManyField(Nganh)

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

    def __str__(self):
        return "CO" + self.stt.__str__() + " - " + self.muc_tieu_mon_hoc.__str__()


class HocLieu(BaseModel):
    ten_hoc_lieu = models.CharField(max_length=500)
    ke_hoach_giang_day = models.ManyToManyField(KeHoachGiangDay)
    de_cuong_mon_hoc = models.ManyToManyField(DeCuongMonHoc)

    def __str__(self):
        return self.ten_hoc_lieu


class Diem(BaseModel):
    class PhanLoaiDiem(models.TextChoices):
        QuaTrinh = 'QT'
        GiuaKy = 'GK'
        CuoiKy = 'CK'
    ty_trong = models.FloatField(default=0)
    hinh_thuc_danh_gia = models.CharField(max_length=50)
    de_cuong_mon_hoc = models.ForeignKey(DeCuongMonHoc, on_delete=models.CASCADE)
    chuan_dau_ra_mon_hoc = models.ManyToManyField(ChuanDauRaMonHoc)
    phan_loai = models.CharField(max_length=2, choices=PhanLoaiDiem.choices)

    def __str__(self):
        return self.phan_loai.__str__() + " - " + self.hinh_thuc_danh_gia.__str__() + " - " + self.de_cuong_mon_hoc.__str__()