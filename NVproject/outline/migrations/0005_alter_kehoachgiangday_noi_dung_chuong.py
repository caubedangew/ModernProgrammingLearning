# Generated by Django 4.2.11 on 2024-05-24 09:54

import ckeditor.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outline', '0004_remove_decuongmonhoc_nam_bien_soan_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='kehoachgiangday',
            name='noi_dung_chuong',
            field=ckeditor.fields.RichTextField(),
        ),
    ]
