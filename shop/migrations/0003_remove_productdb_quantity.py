# Generated by Django 5.1.3 on 2024-11-13 14:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0002_alter_productdb_user"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="productdb",
            name="quantity",
        ),
    ]
