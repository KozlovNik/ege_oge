from django.forms import ModelForm
from .models import SubmittedTest


class NumForm(ModelForm):
    class Meta:
        model = SubmittedTest
        fields = ['question1', 'question2', 'question3', 'question4', 'question5', 'question6', 'question7', 'question8',
                  'question9', 'question10', 'question11', 'question12', 'question13', 'question14', 'question15',
                  'question16', 'question17', 'question18', 'question19', 'question20']
        labels = {
            'question1': 'Ответ: ',
            'question2': 'Ответ: ',
            'question3': 'Ответ: ',
            'question4': 'Ответ: ',
            'question5': 'Ответ: ',
            'question6': 'Ответ: ',
            'question7': 'Ответ: ',
            'question8': 'Ответ: ',
            'question9': 'Ответ: ',
            'question10': 'Ответ: ',
            'question11': 'Ответ: ',
            'question12': 'Ответ: ',
            'question13': 'Ответ: ',
            'question14': 'Ответ: ',
            'question15': 'Ответ: ',
            'question16': 'Ответ: ',
            'question17': 'Ответ: ',
            'question18': 'Ответ: ',
            'question19': 'Ответ: ',
            'question20': 'Ответ: ',
        }
