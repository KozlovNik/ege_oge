# Generated by Django 2.2.3 on 2019-08-25 06:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ege', '0007_auto_20190824_1028'),
    ]

    operations = [
        migrations.AddField(
            model_name='question',
            name='audio_file',
            field=models.FileField(blank=True, null=True, upload_to=''),
        ),
    ]
