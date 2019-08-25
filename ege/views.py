from django.shortcuts import render, HttpResponse, get_object_or_404, redirect, get_list_or_404
from .models import ExamTest, Question, Subject, Exam, SubmittedTest
from .form import NumForm
from django.contrib.auth.forms import User
from django.contrib.auth.decorators import login_required
# from django.contrib.auth import
from itertools import zip_longest


# Функция возвращает query сет с фильтром на экзамен.
# 1 - ЕГЭ
# 2 - ОГЭ
def choose_exam(exam):
    ege_tests = Subject.objects.filter(type_of_exam_id=1).order_by('id')
    oge_tests = Subject.objects.filter(type_of_exam_id=2).order_by('id')
    return ege_tests if exam == 'ege' else oge_tests


def index(request, **kwargs):
    subjects = choose_exam('oge') if '/oge/' in request.path else choose_exam('ege')
    tests = Subject.objects.get(slug=kwargs['slug']).examtest_set.all().order_by('id')[:13] if kwargs else ''
    context = {
        'subjects': subjects.order_by('name'),
        'tests': tests,
    }
    return render(request, 'ege/index.html', context)


def show_all_tests(request, **kwargs):
    tests = Subject.objects.get(slug=kwargs['subj_slug']).examtest_set.all().order_by('id') if kwargs else ''
    subj = Subject.objects.get(slug=kwargs['subj_slug'])
    context = {
        'subj': subj,
        'tests': tests
    }
    return render(request, 'ege/show_all_tests.html', context)


def show_test(request, **kwargs):
    ex_test = get_object_or_404(ExamTest, slug=kwargs['exam_test_slug'])
    questions = ex_test.question_set.all()

    if request.method == 'POST':
        question_data = [question.right_answer for question in questions]
        form = NumForm(request.POST)
        if form.is_valid():
            form_data = [form.cleaned_data[i] for i in form.cleaned_data]
            if request.user.is_authenticated:
                try:
                    # Если номер теста, который прошел заригистрированный пользователь,
                    # присутствует в таблице submittedtest, значит тест уже был когда-то пройден
                    # и идет дальнейшее пересохранение результатов
                    test_model = request.user.submittedtest_set.get(num_of_test_id=ex_test.id)
                    updated_form = NumForm(request.POST, instance=test_model)
                    updated_form.save()
                    updated_form = updated_form.cleaned_data
                    form_data = [updated_form[i] for i in updated_form]
                    context = zipped_context(form_data, question_data, blank_form=False)
                    return render(request, 'ege/results.html', context)
                except SubmittedTest.DoesNotExist:
                    pass
                except User.DoesNotExist:
                    pass

                # Условие отрабатывается в том случае, если зарегистрированный
                # пользователь не проходил данный тест. Производится сохранение значений формы
                # в новую переменную и их перенос в базу данных.
                new_form = form.save(commit=False)
                new_form.num_of_test = ex_test
                new_form.user = request.user
                new_form.save()

            # Создание zip-объекта для итерации по двум значениям
            # через созданную функцию zipped_context и результатов теста
            context = zipped_context(form_data, question_data, blank_form=False)
            return render(request, 'ege/results.html', context)
    else:
        form = NumForm()
        # Создание zip-объекта для вывода одновременного вывода формы с полем ввода ответа
        # и данных из модели со всем списком вопросов
        context = zipped_context(form, questions)
        return render(request, 'ege/show_test.html', context)


# Функция для объединения полей ввода для ответов и данных модели с вопросами
# Если blank_form = False, то в словарь также добавляются данные с результатами теста
def zipped_context(form, questions, blank_form=True):
    zipped_files = zip_longest(form, questions)
    if blank_form:
        zp = {
            'zipped_files': zipped_files,
        }
        return zp
    else:
        percent_of_right_answers = result_of_test(zipped_files)
        zipped_files = zip_longest(form, questions)
        zp = {
            'zipped_files': zipped_files,
            'percent': percent_of_right_answers,
        }
        return zp


# Функция высчитывает процентное соотношение правильных ответов
# В качестве аргумента принимает zip-объект
def result_of_test(z_file):
    number_of_questions = 0
    number_correct_answers = 0
    for a, b in z_file:
        number_of_questions += 1
        if str(a).lower() == str(b).lower():
            number_correct_answers += 1
    percent = round((number_correct_answers / number_of_questions * 100), 1)
    return percent


@login_required
def profile(request, **kwargs):
    usr_tests = get_list_or_404(request.user.submittedtest_set.all())
    context = {
        'usr_tests': usr_tests
    }
    return render(request, 'ege/profile.html', context)


@login_required
def submitted_test(request, **kwargs):
    # ex_test = get_object_or_404(ExamTest, slug=kwargs['exam_test_slug'])
    # questions = ex_test.question_set.all()
    usr_title = request.user.submittedtest_set.get(id=kwargs['id'])
    usr_test = usr_title.num_of_test.question_set.all()
    print(usr_test)
    usr_answers = [getattr(usr_title, i) for i in dir(usr_title) if i.startswith('question')]
    # for i in dir(usr_answers):
    #     if i.startswith('question'):
    #         print(getattr(usr_answers, i))
    zipped_files = zip(usr_test, usr_answers)
    context = {
        'zipped_files': zipped_files,
        'usr_title': usr_title
    }
    return render(request, 'ege/submitted_test.html', context)
