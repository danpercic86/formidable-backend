# Generated by Django 3.2a1 on 2021-02-15 17:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('formidable', '0009_auto_20210215_1850'),
    ]

    operations = [
        migrations.RemoveConstraint(
            model_name='validator',
            name='validator_type_valid',
        ),
        migrations.AlterField(
            model_name='validator',
            name='type',
            field=models.CharField(choices=[('minlength', 'Minimum length'), ('maxlength', 'Maximum length'), ('email', 'Email'), ('pattern', 'Regular expression')], default=None, max_length=10, verbose_name='type'),
        ),
        migrations.AddConstraint(
            model_name='validator',
            constraint=models.CheckConstraint(check=models.Q(type__in=['minlength', 'maxlength', 'email', 'pattern']), name='validator_type_valid'),
        ),
    ]
