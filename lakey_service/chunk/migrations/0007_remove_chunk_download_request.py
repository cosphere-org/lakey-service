# Generated by Django 2.1.10 on 2019-08-21 12:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('chunk', '0006_chunk_download_request'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='chunk',
            name='download_request',
        ),
    ]
