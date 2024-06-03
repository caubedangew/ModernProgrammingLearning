from django.contrib import admin

from outline.models import (User, GiangVien, SinhVien, Khoa, Nganh, MonHoc, Chuong,
                            DeCuongMonHoc, KeHoachGiangDay, HoatDongDayVaHoc, LoaiCDRCTDT,
                            ChuanDauRaCTDT, ChuanDauRaMonHoc, HocLieu, Diem, MucTieuMonHoc)
from django.utils.html import mark_safe
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CourseAppAdminSite(admin.AdminSite):
    site_header = "Hệ thống quản lý việc biên soạn đề cương"


class UserAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "username", "user_role", "is_superuser"]
    search_fields = ["first_name", "user_role"]
    readonly_fields = ["avatar"]
    list_editable = ["user_role"]

    def avatar(self, obj):
        if obj:
            return mark_safe(f'<img src="/static/{obj.avatar}" width="120" />')


class LecturerAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "title", "degree", "sex", "date_of_birth"]
    search_fields = ["id", "first_name", "degree"]


class StudentAdmin(admin.ModelAdmin):
    list_display = ["last_name", "first_name", "sex", "date_of_birth", "nganh"]
    search_fields = ["id", "first_name"]
    list_filter = ["nganh"]


class BranchAdmin(admin.ModelAdmin):
    list_display = ["ten_nganh", "khoa"]
    list_filter = ["khoa"]


class CourseAdmin(admin.ModelAdmin):
    list_display = ["ten_mon_hoc", "ten_mon_hoc_ta",
                    "so_tin_chi_ly_thuyet", "so_tin_chi_thuc_hanh", ]
    readonly_fields = ["so_tin_chi"]
    search_fields = ["ten_mon_hoc", "ten_mon_hoc_ta"]
    
    
class ChapterAdmin(admin.ModelAdmin):
    list_display = ["so_thu_tu_chuong", "ten_chuong", "mon_hoc"]
    search_fields = ["mon_hoc"]


class TeachingPlanInlineAdmin(admin.StackedInline):
    model = KeHoachGiangDay
    fk_name = "de_cuong_mon_hoc"


class CourseObjectiveInlineAdmin(admin.StackedInline):
    model = MucTieuMonHoc
    fk_name = "de_cuong_mon_hoc"


class ScoreInlineAdmin(admin.TabularInline):
    model = Diem
    fk_name = "de_cuong_mon_hoc"


class OutlineAdmin(admin.ModelAdmin):
    list_display = ["giang_vien_bien_soan", "mon_hoc", "updated_date"]
    search_fields = ["giang_vien_bien_soan", "mon_hoc"]
    inlines = [CourseObjectiveInlineAdmin, TeachingPlanInlineAdmin, ScoreInlineAdmin]


class TeachingPlanAdmin(admin.ModelAdmin):
    list_display = ["tuan", "chuong", "de_cuong_mon_hoc"]
    search_fields = ["de_cuong_mon_hoc"]


class ActivityAdmin(admin.ModelAdmin):
    list_display = ["so_tiet", "loai_hoat_dong", "ke_hoach_giang_day"]
    search_fields = ["ke_hoach_giang_day"]


class ReferenceAdmin(admin.ModelAdmin):
    list_display = ["id", "ten_hoc_lieu"]
    search_fields = ["ten_hoc_lieu"]


class ScoreAdmin(admin.ModelAdmin):
    list_display = ["de_cuong_mon_hoc", "phan_loai", "hinh_thuc_danh_gia"]
    search_fields = ["de_cuong_mon_hoc"]


admin_site = CourseAppAdminSite()

admin_site.register(User, UserAdmin)
admin_site.register(GiangVien, LecturerAdmin)
admin_site.register(SinhVien, StudentAdmin)
admin_site.register(Khoa)
admin_site.register(Nganh, BranchAdmin)
admin_site.register(MonHoc, CourseAdmin)
admin_site.register(Chuong, ChapterAdmin)
admin_site.register(DeCuongMonHoc, OutlineAdmin)
admin_site.register(KeHoachGiangDay, TeachingPlanAdmin)
admin_site.register(MucTieuMonHoc)
admin_site.register(HoatDongDayVaHoc, ActivityAdmin)
admin_site.register(LoaiCDRCTDT)
admin_site.register(ChuanDauRaCTDT, )
admin_site.register(ChuanDauRaMonHoc)
admin_site.register(HocLieu, ReferenceAdmin)
admin_site.register(Diem, ScoreAdmin)
