# Generated by Django 3.2a1 on 2021-02-15 16:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("formidable", "0008_auto_20210213_1700"),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name="validator",
            name="validator_type_valid",
        ),
        migrations.AlterField(
            model_name="validator",
            name="type",
            field=models.CharField(
                choices=[
                    ("minLength", "Minimum length"),
                    ("maxLength", "Maximum length"),
                    ("email", "Email"),
                    ("pattern", "Regular expression"),
                ],
                default=None,
                max_length=10,
                verbose_name="type",
            ),
        ),
        migrations.AddConstraint(
            model_name="validator",
            constraint=models.CheckConstraint(
                check=models.Q(type__in=["minLength", "maxLength", "email", "pattern"]),
                name="validator_type_valid",
            ),
        ),
    ]
