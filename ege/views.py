from django.shortcuts import render, HttpResponse, get_object_or_404, redirect
from .models import ExamTest, Question, Subject, Exam, SubmittedTest
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
        form = NumForm(request.POST)
        if form.is_valid():

            # Если True, значит пользователь уже когда-то проходил тест
            try:
                usr = User.objects.get(pk=request.user.id)
                test_model = usr.submittedtest_set.get(num_of_test_id=ex_test.id)
                updated_form = NumForm(request.POST, instance=test_model)
                updated_form.save()
                context = zipped_context(updated_form, questions)
                return render(request, 'ege/results.html', context)
            except SubmittedTest.DoesNotExist:
                pass
            except User.DoesNotExist:
                pass

            if request.user.is_authenticated:
                save_user_test(request, form, ex_test)
            context = zipped_context(form, questions)
            return render(request, 'ege/results.html', context)
    else:
        form = NumForm()
        context = zipped_context(form, questions)
        return render(request, 'ege/show_test.html', context)




def zipped_context(form, questions):
    zipped_files = zip(form, questions)
    zp = {
        'zipped_files': zipped_files,
    }
    return zp


def save_user_test(request, form, number_of_test):
    usr = User.objects.get(username=request.user)
    new_form = form.save(commit=False)
    new_form.num_of_test = number_of_test
    new_form.save()
    new_form.users.add(usr)
