# Generated by Django 3.2.13 on 2022-11-06 16:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('articles', '0003_auto_20221107_0113'),
    ]

    operations = [
        migrations.AlterField(
            model_name='movie',
            name='genre',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
