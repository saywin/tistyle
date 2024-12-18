# Generated by Django 5.1.3 on 2024-11-20 08:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0008_alter_productdb_article"),
    ]

    operations = [
        migrations.AlterField(
            model_name="productdb",
            name="slug",
            field=models.SlugField(
                blank=True, max_length=255, unique=True, verbose_name="URL"
            ),
        ),
    ]
