# Generated by Django 4.2.11 on 2024-06-15 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("outline", "0019_remove_decuongmonhoc_hoc_lieu_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="user",
            name="avatar",
            field=models.ImageField(upload_to="static/outline/%Y/%m"),
        ),
    ]