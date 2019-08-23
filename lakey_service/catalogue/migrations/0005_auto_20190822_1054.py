# Generated by Django 2.1.10 on 2019-08-22 10:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('catalogue', '0004_catalogueitem_data_path'),
    ]

    operations = [
        migrations.AlterField(
            model_name='catalogueitem',
            name='data_path',
            field=models.CharField(
                blank=True,
                max_length=256,
                null=True,
                unique=True),
        ),
    ]
