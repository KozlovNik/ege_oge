from django.forms import ModelForm
from .models import SubmittedTest


class NumForm(ModelForm):
    class Meta:
        model = SubmittedTest
        fields = ['question1', 'question2', 'question3']
        labels = {
            'question1': 'Ответ: ',
            'question2': 'Ответ: ',
            'question3': 'Ответ: ',
        }
