# Generated by Django 3.2.7 on 2021-09-04 14:43

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("formidable", "0025_auto_20210904_0354"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="form",
            options={
                "ordering": ["order_index"],
                "verbose_name": "form",
                "verbose_name_plural": "forms",
            },
        ),
        migrations.AddField(
            model_name="form",
            name="order_index",
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name="historicalform",
            name="order_index",
            field=models.PositiveIntegerField(default=0),
        ),
    ]