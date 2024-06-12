# Generated by Django 4.2.11 on 2024-06-11 14:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('outline', '0014_remove_muctieumonhoc_chuan_dau_ra_ctdt'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='hoatdongdayvahoc',
            name='chuan_dau_ra_mon_hoc',
        ),
        migrations.AddField(
            model_name='kehoachgiangday',
            name='bai_danh_gia',
            field=models.ManyToManyField(blank=True, to='outline.diem'),
        ),
        migrations.AddField(
            model_name='kehoachgiangday',
            name='chuan_dau_ra_mon_hoc',
            field=models.ManyToManyField(to='outline.chuandauramonhoc'),
        ),
        migrations.AlterField(
            model_name='kehoachgiangday',
            name='hoc_lieu',
            field=models.ManyToManyField(blank=True, to='outline.hoclieu'),
        ),
    ]