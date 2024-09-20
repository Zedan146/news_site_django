from django.shortcuts import get_object_or_404, redirect, render
# ListView - для работы со списками, DetailView - для работы с одним объектом, CreateView - для работы с формой
from django.views.generic import ListView, DetailView, CreateView
from django.urls import reverse_lazy
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.contrib import messages
from django.contrib.auth import login, logout
from django.core.mail import send_mail

from .models import News, Category
from .forms import NewsForm, UserRegisterForm, UserLoginForm, ContactForm
from .utils import MyMixin


class HomeNews(MyMixin, ListView):  # Класс равносилен функции index ниже
    model = News  # Определяем модель, с которой будем работать
    template_name = 'news/index.html'  # Указываем имя шаблона, к которому будет ссылаться класс
    context_object_name = 'news'  # Указываем имя объекта, с которым хотим рабоатать
    paginate_by = 2  # Пагинация страниц

    # Переопределяем метод для отображения динамичных данных
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper('Главная страница')
        context['mixin_prop'] = self.get_prop()
        return context

    # Переопределяем метод для фильтрации отображаемых данных
    def get_queryset(self):
        return News.objects.filter(is_published=True).select_related('category')


class NewsByCategory(MyMixin, ListView):  # Класс равносилен функции get_category ниже
    model = News
    template_name = 'news/index.html'
    context_object_name = 'news'
    allow_empty = False  # Запрещаем показ пустых списков
    paginate_by = 2

    # Переопределяем метод для отображения динамичных данных
    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = self.get_upper(Category.objects.get(pk=self.kwargs['category_id']))
        return context

    # Переопределяем метод для фильтрации отображаемых данных
    def get_queryset(self):
        return News.objects.filter(category_id=self.kwargs['category_id'], is_published=True).select_related('category')


class ViewNews(DetailView):  # Класс равносилен функции view_news ниже
    model = News
    template_name = 'news/view_news.html'
    context_object_name = 'news_item'


class CreateNews(LoginRequiredMixin, CreateView):  # Класс равносилен функции add_news ниже
    form_class = NewsForm  # Определяем форму, с которой будем работать
    template_name = 'news/add_news.html'
    login_url = '/admin/'
    # success_url = reverse_lazy('home') - выполняет редирект после заполнения формы на домашнюю страницу


def register(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, 'Вы успешно зарегестрировались')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form = UserRegisterForm()
    return render(request, 'news/register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = UserLoginForm()
    return render(request, 'news/login.html', {'form': form})


def user_logout(request):
    logout(request)
    return redirect('login')


def contact(request):
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            mail = send_mail(form.cleaned_data['subject'], form.cleaned_data['content'],
                             'danila.zenkovitch17@yandex.ru',
                             ['danila.zenkovitch13@yandex.ru'], fail_silently=True)
            if mail:
                messages.success(request, 'Письмо отправлено')
                return redirect('contact')
            else:
                messages.error(request, 'Ошибка отправки')
        else:
            messages.error(request, 'Ошибка валидации')
    else:
        form = ContactForm()
    return render(request, 'news/test.html', {'form': form})

# def index(request):
#     news = News.objects.all()
#     context = {
#         'news': news,
#         'title': 'Список новостей',
#     }
#     return render(request, 'news/index.html', context)


# def get_category(request, category_id):
#     news = News.objects.filter(category_id=category_id)
#     category = Category.objects.get(pk=category_id)
#     context = {
#         'news': news,
#         'category': category,
#     }
#     return render(request, 'news/category.html', context)


# def view_news(request, news_id):
#     # news_item = News.objects.get(pk=news_id)
#     news_item = get_object_or_404(News, pk=news_id)
#     return render(request, 'news/view_news.html', {'news_item': news_item})


# def add_news(request):
#     if request.method == 'POST':
#         form = NewsForm(request.POST)
#         if form.is_valid():
#             news = form.save()
#             return redirect(news)
#     else:
#         form = NewsForm()
#     return render(request, 'news/add_news.html', {'form': form})

#  Тестовая пагинация страниц через функции
# def test_paginator(request):
#     objects = ["john1", "paul2", "george3", "ringo4", "john5", "paul6", "george7"]
#     paginator = Paginator(objects, 2)
#     page_num = request.GET.get('page', 1)
#     page_obj = paginator.get_page(page_num)
#     return render(request, 'news/test.html', {'page_obj': page_obj})
