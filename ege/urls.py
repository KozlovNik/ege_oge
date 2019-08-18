from django.urls import path, re_path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('ege/', views.index, name='exam_ege'),
    path('oge/', views.index, name='exam_oge'),
    path('ege/<slug>/', views.index, name='subj_ege'),
    path('oge/<slug>/', views.index, name='subj_oge'),
    re_path(r'(?P<exam>(ege|oge))/(?P<subj_slug>[\w-]+)/all-tests', views.show_all_tests, name='show_all_tests'),
    path('<exam_test_slug>/', views.show_test, name='exam_test'),
    path('hello/results/', views.show_results, name='results'),
]
