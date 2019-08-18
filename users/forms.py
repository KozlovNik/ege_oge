from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm


class UserRegisterForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        for item in ['username', 'password1', 'password2']:
            self.fields[item].help_text = None

        self.fields['username'].label = 'Имя пользователя'
        self.fields['password1'].label = 'Пароль'
        self.fields['password2'].label = 'Повторите пароль'
        self.fields['email'].label = 'Email'

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']


