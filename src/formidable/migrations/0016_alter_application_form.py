# Generated by Django 3.2.3 on 2021-05-17 21:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("formidable", "0015_auto_20210517_0408"),
    ]

    operations = [
        migrations.AlterField(
            model_name="application",
            name="form",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="applications",
                related_query_name="application",
                to="formidable.form",
                verbose_name="form this response belongs to",
            ),
        ),
    ]
