# Generated by Django 4.2.11 on 2024-06-13 16:05

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('outline', '0018_remove_hoclieu_stt_alter_diem_phan_loai'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='decuongmonhoc',
            name='hoc_lieu',
        ),
        migrations.RemoveField(
            model_name='hoclieu',
            name='de_cuong_mon_hoc',
        ),
        migrations.CreateModel(
            name='HocLieu_DeCuongMonHoc',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('stt', models.IntegerField(default=0)),
                ('de_cuong_mon_hoc', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outline.decuongmonhoc')),
                ('hoc_lieu', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='outline.hoclieu')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
