# Generated by Django 4.2.11 on 2024-06-05 14:21

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('outline', '0013_mucdodapung'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='muctieumonhoc',
            name='chuan_dau_ra_ctdt',
        ),
    ]
