from django.db import models
from django.db.models.signals import pre_save
from django.utils.text import slugify
from transliterate import translit
from django.contrib.auth.models import User


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
        ordering = ['id']


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


def image_folder(instance, filename):
    instance.slug = slugify(translit(instance.name, reversed=True))
    filename = instance.slug + '.' + filename.split('.')[1]
    return filename


class Question(models.Model):
    name = models.CharField(max_length=50, verbose_name='Номер вопроса', unique=True)
    description1 = models.TextField(max_length=5000, verbose_name='Описание вопроса 1', null=True)
    description2 = models.TextField(max_length=5000, verbose_name='Описание вопроса 2', blank=True, null=True)
    right_answer = models.CharField(max_length=500, verbose_name="Правильный ответ", blank=True)
    audio_file = models.FileField(blank=True, null=True)
    image = models.ImageField(blank=True, upload_to=image_folder)
    exam_tests = models.ManyToManyField(ExamTest, blank=True)
    order_num = models.IntegerField(null=True, blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Вопрос'
        verbose_name_plural = 'Вопросы'
        ordering = ['order_num']


class SubmittedTest(models.Model):
    user = models.ForeignKey(User, blank=True, null=True, on_delete=models.CASCADE)
    question1 = models.CharField(max_length=30, blank=True)
    question2 = models.CharField(max_length=30, blank=True)
    question3 = models.CharField(max_length=30, blank=True)
    question4 = models.CharField(max_length=30, blank=True)
    question5 = models.CharField(max_length=30, blank=True)
    question6 = models.CharField(max_length=30, blank=True)
    question7 = models.CharField(max_length=30, blank=True)
    question8 = models.CharField(max_length=30, blank=True)
    question9 = models.CharField(max_length=30, blank=True)
    question10 = models.CharField(max_length=30, blank=True)
    question11 = models.CharField(max_length=30, blank=True)
    question12 = models.CharField(max_length=30, blank=True)
    question13 = models.CharField(max_length=30, blank=True)
    question14 = models.CharField(max_length=30, blank=True)
    question15 = models.CharField(max_length=30, blank=True)
    question16 = models.CharField(max_length=30, blank=True)
    question17 = models.CharField(max_length=30, blank=True)
    question18 = models.CharField(max_length=30, blank=True)
    question19 = models.CharField(max_length=30, blank=True)
    question20 = models.CharField(max_length=30, blank=True)
    date = models.DateTimeField(auto_now_add=True)
    num_of_test = models.ForeignKey(ExamTest, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.num_of_test.__str__()

    # def get_absolute_url(self):
    #     return reverse('submitted_test', args=[self.num_of_test])

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


def pre_save_question(sender, instance, *args, **kwargs):
    if not instance.order_num:
        instance.order_num = int(instance.name.split(' ')[1])


pre_save.connect(pre_save_subject_receiver, sender=Subject)
pre_save.connect(pre_save_exam_test, sender=ExamTest)
pre_save.connect(pre_save_question, sender=Question)
