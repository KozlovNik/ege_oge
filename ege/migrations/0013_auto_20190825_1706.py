# Generated by Django 2.2.3 on 2019-08-25 14:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('ege', '0012_question_order_num'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='question',
            options={'ordering': ['order_num'], 'verbose_name': 'Вопрос', 'verbose_name_plural': 'Вопросы'},
        ),
    ]