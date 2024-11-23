# Generated by Django 5.1.3 on 2024-11-21 10:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("review", "0005_alter_reviewdb_text"),
    ]

    operations = [
        migrations.AlterField(
            model_name="reviewdb",
            name="grade",
            field=models.IntegerField(
                blank=True,
                choices=[
                    ("5", "Відмінно"),
                    ("4", "Добре"),
                    ("3", "Нормально"),
                    ("2", "Погано"),
                    ("1", "Жахливо"),
                ],
                max_length=20,
                null=True,
                verbose_name="Оцінка",
            ),
        ),
    ]