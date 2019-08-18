from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.contrib.auth.models import User
from datetime import datetime


class Exam(models.Model):
    name = models.CharField(max_length=50, verbose_name='Вид экзамена')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вид экзамена'
        verbose_name_plural = 'Виды экзамена'


class Subject(models.Model):
    name = models.CharField(max_length=50, verbose_name='Предмет')
    slug = models.SlugField(max_length=150, unique=True, blank=True)
    type_of_exam = models.ForeignKey(Exam, on_delete=models.PROTECT)

    def __str__(self):
        name = self.name + '-' + str(self.type_of_exam)
        return name

    class Meta:
        verbose_name_plural = "Предметы"
        verbose_name = 'Предмет'


class ExamTest(models.Model):
    name = models.CharField(max_length=50, verbose_name='Вариант')
    subject = models.ForeignKey(Subject, on_delete=models.PROTECT)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def __str__(self):
        return self.name + '(' + str(self.subject) + ')'

    class Meta:
        verbose_name = 'Вариант'
        verbose_name_plural = 'Варианты'
        ordering = ['subject']


class Question(models.Model):
    name = models.CharField(max_length=50, verbose_name='Номер вопроса', unique=True)
    description = models.TextField(max_length=500, verbose_name='Вопрос')
    right_answer = models.CharField(max_length=500, verbose_name="Правильный ответ", blank=True)
    image = models.ImageField(blank=True)
    answer = models.TextField(max_length=500, blank=True, verbose_name='Варианты ответов')
    exam_tests = models.ManyToManyField(ExamTest, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['pk']


class SubmittedTest(models.Model):
    users = models.ManyToManyField(User, blank=True)
    q1 = models.CharField(max_length=30, blank=True)
    q2 = models.CharField(max_length=30, blank=True)
    q3 = models.CharField(max_length=30, blank=True)
    date = models.DateTimeField(auto_now=True)
    # num_of_test = models.ManyToManyField(ExamTest)

    class Meta:
        verbose_name = 'Решенный вариант'
        verbose_name_plural = 'Решенные варианты'


def pre_save_subject_receiver(sender, instance, *args, **kwargs):
    if not instance.slug:
        slug_subj = slugify(translit(instance.name, reversed=True))
        slug_exam = Exam.objects.get(pk=instance.type_of_exam_id)
        instance.slug = slug_subj + '-' + translit(slug_exam.name.lower(), reversed=True)


def pre_save_exam_test(sender, instance, *args, **kwargs):
    if not instance.slug:
        test_slug = instance.name.split(' ')
        test_slug[0] = test_slug[0][0:3]
        test_slug = translit('-'.join(test_slug).lower(), reversed=True)
        subj_slug = Subject.objects.get(pk=instance.subject_id).slug
        instance.slug = test_slug + '-' + subj_slug


pre_save.connect(pre_save_subject_receiver, sender=Subject)
pre_save.connect(pre_save_exam_test, sender=ExamTest)
ghfghfgh