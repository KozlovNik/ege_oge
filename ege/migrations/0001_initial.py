# Generated by Django 2.2.4 on 2019-08-22 06:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Exam',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Вид экзамена')),
            ],
            options={
                'verbose_name': 'Вид экзамена',
                'verbose_name_plural': 'Виды экзамена',
            },
        ),
        migrations.CreateModel(
            name='ExamTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Вариант')),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
            ],
            options={
                'verbose_name': 'Вариант',
                'verbose_name_plural': 'Варианты',
                'ordering': ['subject'],
            },
        ),
        migrations.CreateModel(
            name='SubmittedTest',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question1', models.CharField(blank=True, max_length=30)),
                ('question2', models.CharField(blank=True, max_length=30)),
                ('question3', models.CharField(blank=True, max_length=30)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('num_of_test', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='ege.ExamTest')),
                ('users', models.ManyToManyField(blank=True, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Решенный вариант',
                'verbose_name_plural': 'Решенные варианты',
            },
        ),
        migrations.CreateModel(
            name='Subject',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, verbose_name='Предмет')),
                ('slug', models.SlugField(blank=True, max_length=150, unique=True)),
                ('type_of_exam', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ege.Exam')),
            ],
            options={
                'verbose_name': 'Предмет',
                'verbose_name_plural': 'Предметы',
                'ordering': ['id'],
            },
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50, unique=True, verbose_name='Номер вопроса')),
                ('description', models.TextField(max_length=500, verbose_name='Вопрос')),
                ('right_answer', models.CharField(blank=True, max_length=500, verbose_name='Правильный ответ')),
                ('image', models.ImageField(blank=True, upload_to='')),
                ('answer', models.TextField(blank=True, max_length=500, verbose_name='Варианты ответов')),
                ('exam_tests', models.ManyToManyField(blank=True, to='ege.ExamTest')),
            ],
            options={
                'verbose_name': 'Вопрос',
                'verbose_name_plural': 'Вопросы',
                'ordering': ['pk'],
            },
        ),
        migrations.AddField(
            model_name='examtest',
            name='subject',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='ege.Subject'),
        ),
    ]
