from django import forms
from .models import News
import re
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.models import User
from captcha.fields import CaptchaField


# Создаем класс формы связанной с моделью, для добавления новостей
class NewsForm(forms.ModelForm):
    class Meta:
        model = News    # Указываем с какой моделью будет связана форма
        fields = ['title', 'content', 'is_published', 'category']   # Указываем нужные поля для формы
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'category': forms.Select(attrs={'class': 'form-control'}),
        }   # Добавляем классы форм отображения полей

    # Создание собственного валидатора для поля title
    def clean_title(self):
        title = self.cleaned_data['title']
        if re.match(r'\d', title):
            raise ValidationError('Название не должно начинаться с цифры')
        return title


# Класс формы регистрации
class UserRegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email', widget=forms.EmailInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')


# Класс формы авторизации
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(label='Имя пользователя', widget=forms.TextInput(attrs={'class': 'form-control'}))
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(attrs={'class': 'form-control'}))


class ContactForm(forms.Form):
    subject = forms.CharField(label='Тема', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст', widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 5}))
    captcha = CaptchaField()


"""
Пример реализации формы несвязанной с моделью

class NewsForm(forms.Form):
    title = forms.CharField(max_length=150, label='Название ', widget=forms.TextInput(attrs={'class': 'form-control'}))
    content = forms.CharField(label='Текст ', required=False, widget=forms.Textarea(attrs={'class': 'form-control'}))
    is_published = forms.BooleanField(label='Опубликовано? ', initial=True)
    category = forms.ModelChoiceField(empty_label='Выберите категорию', label='Категория ',
                                      queryset=Category.objects.all(),
                                      widget=forms.Select(attrs={'class': 'form-control'}))
"""