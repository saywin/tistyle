# Generated by Django 5.1.3 on 2024-11-26 13:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0003_cartitemdb_size"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cartdb",
            options={
                "ordering": ("-created_at",),
                "verbose_name": "Замовлення",
                "verbose_name_plural": "Замовлення",
            },
        ),
    ]
