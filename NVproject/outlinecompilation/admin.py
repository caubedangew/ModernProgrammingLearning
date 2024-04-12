from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe
from outlinecompilation.models import (User, GiangVien, SinhVien, Khoa, Nganh,
                                       MonHoc, Chuong, DeCuongMonHoc, KeHoachGiangDay,
                                       HoatDongDayVaHoc, LoaiCDRCTDT, ChuanDauRaCTDT,
                                       MucTieuMonHoc, ChuanDauRaMonHoc, HocLieu, Diem)


class UserAdminSite(admin.ModelAdmin):
    def read_avatar(self, user):
        return mark_safe(f"<img src='{user.avatar}' width='200'/>")


# Register your models here.
class ChuongAdminSite(admin.ModelAdmin):
    list_display = ['so_thu_tu_chuong', 'ten_chuong', 'mon_hoc']


class DeCuongMonHocAdminSite(admin.ModelAdmin):
    list_display = ['mon_hoc', 'giang_vien_bien_soan']


admin.site.register(User)
admin.site.register(GiangVien)
admin.site.register(SinhVien)
admin.site.register(Khoa)
admin.site.register(Nganh)
admin.site.register(MonHoc)
admin.site.register(Chuong, ChuongAdminSite)
admin.site.register(DeCuongMonHoc, DeCuongMonHocAdminSite)
admin.site.register(KeHoachGiangDay)
admin.site.register(HoatDongDayVaHoc)
admin.site.register(LoaiCDRCTDT)
admin.site.register(ChuanDauRaCTDT)
admin.site.register(ChuanDauRaMonHoc)
admin.site.register(MucTieuMonHoc)
admin.site.register(HocLieu)
admin.site.register(Diem)


