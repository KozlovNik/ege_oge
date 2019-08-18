from django.contrib import admin
from .models import ExamTest, Question, Subject, Exam, SubmittedTest


admin.site.register(ExamTest)
admin.site.register(Question)
admin.site.register(Subject)
admin.site.register(Exam)
admin.site.register(SubmittedTest)
