# Generated by Django 2.2.3 on 2019-08-25 14:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ege', '0014_auto_20190825_1708'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['order_num'], 'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопросы'},
        ),
    ]
