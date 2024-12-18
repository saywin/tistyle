# Generated by Django 5.1.3 on 2024-11-20 14:37

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0001_initial"),
        ("shop", "0009_alter_productdb_slug"),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="Rating",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "grade",
                    models.CharField(
                        choices=[
                            ("1", "Відмінно"),
                            ("2", "Добре"),
                            ("3", "Нормально"),
                            ("4", "Погано"),
                            ("5", "Жахливо"),
                        ],
                        max_length=20,
                        verbose_name="Оцінка",
                    ),
                ),
                (
                    "author",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rating",
                        to=settings.AUTH_USER_MODEL,
                        verbose_name="Автор",
                    ),
                ),
                (
                    "product",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="rating",
                        to="shop.productdb",
                        verbose_name="Товар",
                    ),
                ),
            ],
            options={
                "verbose_name": "Рейтинг",
                "verbose_name_plural": "Рейтинг",
                "db_table": "rating",
            },
        ),
    ]
