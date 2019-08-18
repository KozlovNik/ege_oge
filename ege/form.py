from django.forms import ModelForm
from .models import SubmittedTest


class NumForm(ModelForm):
    class Meta:
        model = SubmittedTest
        fields = ['q1', 'q2', 'q3']
        labels = {
            'q1': 'Ответ: ',
            'q2': 'Ответ: ',
            'q3': 'Ответ: ',
        }
