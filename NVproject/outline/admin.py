from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.hashers import make_password
from django.db.models import Count
from django.template.response import TemplateResponse
from django.urls import path

from outline.models import (User, GiangVien, SinhVien, Khoa, Nganh, MonHoc, Chuong,
                            DeCuongMonHoc, KeHoachGiangDay, HoatDongDayVaHoc, LoaiCDRCTDT,
                            ChuanDauRaCTDT, ChuanDauRaMonHoc, HocLieu, Diem, MucTieuMonHoc)
from django.utils.html import mark_safe
from django import forms
from ckeditor_uploader.widgets import CKEditorUploadingWidget


class CourseAppAdminSite(admin.AdminSite):
    site_header = "Hệ thống quản lý việc biên soạn đề cương"

    # def get_urls(self):
    #     return [
    #         path('course-stats/', self.stats_view)
    #     ] + super().get_urls()

    # def stats_view(self, request):
    #     count = Course.objects.filter(active=True).count()
    #     stats = (Course.objects.annotate(lesson_count=Count("lesson"))
    #                             .values('id', 'name', 'lesson_count'))
    #
    #     return TemplateResponse(request,
    #                             'admin/course-stats.html', {
    #                                 'course_count': count,
    #                                 'course_stats': stats
    #                             })


admin_site = CourseAppAdminSite(name='stats')

admin_site.register(User)
admin_site.register(GiangVien)
admin_site.register(SinhVien)
admin_site.register(Khoa)
admin_site.register(Nganh)
admin_site.register(MonHoc)
admin_site.register(Chuong)
admin_site.register(DeCuongMonHoc)
admin_site.register(KeHoachGiangDay)
admin_site.register(MucTieuMonHoc)
admin_site.register(HoatDongDayVaHoc)
admin_site.register(LoaiCDRCTDT)
admin_site.register(ChuanDauRaCTDT)
admin_site.register(ChuanDauRaMonHoc)
admin_site.register(HocLieu)
admin_site.register(Diem)