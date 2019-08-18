from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import ExamTest, Question, Subject, Exam
from .form import NumForm
from django.contrib.auth.forms import User


# Функция возвращает query сет с фильтром на экзамен.
# 1 - ЕГЭ
# 2 - ОГЭ
def choose_exam(exam):
    ege_tests = Subject.objects.filter(type_of_exam_id=1).order_by('id')
    oge_tests = Subject.objects.filter(type_of_exam_id=2).order_by('id')
    return ege_tests if exam == 'ege' else oge_tests


def index(request, **kwargs):
    subjects = choose_exam('oge') if '/oge/' in request.path else choose_exam('ege')
    tests = Subject.objects.get(slug=kwargs['slug']).examtest_set.all()[:13] if kwargs else ''
    context = {
        'subjects': subjects,
        'tests': tests,
    }
    return render(request, 'ege/index.html', context)


def show_all_tests(request, **kwargs):
    subj = Subject.objects.get(slug=kwargs['subj_slug'])
    context = {
        'subj': subj,
    }
    return render(request, 'ege/show_all_tests.html', context)


def show_test(request, **kwargs):
    ex_test = get_object_or_404(ExamTest, slug=kwargs['exam_test_slug'])
    questions = ex_test.question_set.all()
    if request.method == 'POST':
        form = NumForm(request.POST)
        if form.is_valid():
            zip_files = zip(form, questions)
            context = {
                'zip_files': zip_files,
                'ex_test': ex_test,
            }
            try:
                usr = User.objects.get(username=request.user)
            except User.DoesNotExist:
                guest_user_id = 2
                usr = User.objects.get(id=guest_user_id)
            new_form = form.save()
            new_form.users.add(usr)
            return render(request, 'ege/results.html', context)
    else:
        form = NumForm()
        zip_files = zip(form, questions)
        context = {
            'zip_files': zip_files,
            'ex_test': ex_test,
        }
        return render(request, 'ege/show_test.html', context)


def show_results(request, **kwargs):

    return render(request, 'ege/results.html')
