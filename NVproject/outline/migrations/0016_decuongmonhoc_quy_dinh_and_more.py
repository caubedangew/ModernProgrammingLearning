# Generated by Django 4.2.11 on 2024-06-11 15:42

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outline', '0015_remove_hoatdongdayvahoc_chuan_dau_ra_mon_hoc_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='decuongmonhoc',
            name='quy_dinh',
            field=ckeditor.fields.RichTextField(default='- Sinh viên tham gia đầy đủ các buổi học lý thuyết và thực hành.'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='hoatdongdayvahoc',
            name='cong_viec',
            field=ckeditor.fields.RichTextField(null=True),
        ),
    ]