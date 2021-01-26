# Generated by Django 3.1.5 on 2021-01-21 20:05

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('formidable', '0002_auto_20210121_2159'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Response',
            new_name='Application',
        ),
        migrations.AlterModelOptions(
            name='application',
            options={'verbose_name': 'application', 'verbose_name_plural': 'applications'},
        ),
        migrations.AlterModelOptions(
            name='choice',
            options={'verbose_name': 'choice', 'verbose_name_plural': 'choices'},
        ),
        migrations.AlterModelOptions(
            name='form',
            options={'verbose_name': 'form', 'verbose_name_plural': 'forms'},
        ),
        migrations.AlterModelOptions(
            name='formfield',
            options={'verbose_name': 'field', 'verbose_name_plural': 'fields'},
        ),
        migrations.AlterModelOptions(
            name='responsefield',
            options={'verbose_name': 'response', 'verbose_name_plural': 'responses'},
        ),
        migrations.AlterModelOptions(
            name='validator',
            options={'verbose_name': 'validator', 'verbose_name_plural': 'validators'},
        ),
    ]