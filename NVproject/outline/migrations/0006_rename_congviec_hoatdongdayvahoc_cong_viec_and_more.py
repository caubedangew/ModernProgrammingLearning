# Generated by Django 4.2.11 on 2024-05-26 09:29

import ckeditor.fields
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('outline', '0005_alter_kehoachgiangday_noi_dung_chuong'),
    ]

    operations = [
        migrations.RenameField(
            model_name='hoatdongdayvahoc',
            old_name='congViec',
            new_name='cong_viec',
        ),
        migrations.RenameField(
            model_name='hoatdongdayvahoc',
            old_name='loaiHoatDong',
            new_name='loai_hoat_dong',
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('content', ckeditor.fields.RichTextField(max_length=255)),
                ('outline', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outline.decuongmonhoc')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
