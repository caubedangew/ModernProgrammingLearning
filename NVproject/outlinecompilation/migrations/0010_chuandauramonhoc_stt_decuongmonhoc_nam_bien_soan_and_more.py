# Generated by Django 4.2.11 on 2024-04-10 13:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outlinecompilation', '0009_chuandauractdt_stt_loaicdrctdt_stt'),
    ]

    operations = [
        migrations.AddField(
            model_name='chuandauramonhoc',
            name='stt',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='decuongmonhoc',
            name='nam_bien_soan',
            field=models.IntegerField(default='2024'),
        ),
        migrations.AddField(
            model_name='diem',
            name='phan_loai',
            field=models.CharField(choices=[('QT', 'Quatrinh'), ('GK', 'Giuaky'), ('CK', 'Cuoiky')], default=1, max_length=2),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='muctieumonhoc',
            name='stt',
            field=models.IntegerField(default=0),
        ),
    ]
