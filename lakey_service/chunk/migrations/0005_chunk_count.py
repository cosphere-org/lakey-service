# Generated by Django 2.1.10 on 2019-08-22 11:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('chunk', '0004_remove_chunk_count'),
    ]

    operations = [
        migrations.AddField(
            model_name='chunk',
            name='count',
            field=models.IntegerField(default=None),
        ),
    ]