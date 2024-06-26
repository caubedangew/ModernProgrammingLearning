# Generated by Django 4.2.11 on 2024-04-22 10:02

from django.conf import settings
import django.contrib.auth.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('outline', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Khoa',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('ten_khoa', models.CharField(max_length=50)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Nganh',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('active', models.BooleanField(default=True)),
                ('created_date', models.DateTimeField(auto_now_add=True)),
                ('updated_date', models.DateTimeField(auto_now=True)),
                ('ten_nganh', models.CharField(max_length=50)),
                ('khoa', models.ForeignKey(on_delete=django.db.models.deletion.RESTRICT, to='outline.khoa')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SinhVien',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('nganh', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='outline.nganh')),
            ],
            options={
                'verbose_name': 'Sinh vien',
            },
            bases=('outline.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='GiangVien',
            fields=[
                ('user_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('title', models.CharField(max_length=100)),
                ('degree', models.CharField(max_length=30)),
                ('khoa', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='outline.khoa')),
            ],
            options={
                'verbose_name': 'Giang vien',
            },
            bases=('outline.user',),
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
    ]
