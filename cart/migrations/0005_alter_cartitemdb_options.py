# Generated by Django 5.1.3 on 2024-11-26 14:13

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("cart", "0004_alter_cartdb_options"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="cartitemdb",
            options={
                "ordering": ["-added_at"],
                "verbose_name": "Товар в кошику",
                "verbose_name_plural": "Товари в кошику",
            },
        ),
    ]
