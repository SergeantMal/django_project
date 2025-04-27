from django.http import JsonResponse
import requests
from datetime import datetime
from deep_translator import GoogleTranslator
from django.shortcuts import get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Account, User
from django.db.models import Q
from django.contrib.auth.hashers import make_password
from .forms import UserForm
from .forms import RegisterForm, LoginForm
from django.contrib import messages
from django.shortcuts import render, redirect



def index(request):
    translation = None
    quote = {
        "text": "",
        "author": ""
    }

    if request.method == 'GET':
        try:
            response = requests.get("https://zenquotes.io/api/random")
            data = response.json()[0]
            quote['text'] = data['q']
            quote['author'] = data['a']
        except Exception as e:
            quote['text'] = f"Ошибка загрузки цитаты: {e}"
            quote['author'] = ""

    elif request.method == 'POST':
        quote['text'] = request.POST.get('text', '')
        quote['author'] = request.POST.get('author', '')
        try:
            translation = GoogleTranslator(source='auto', target='ru').translate(quote['text'])
        except Exception:
            translation = "Ошибка перевода."

    return render(request, 'siteapp/index.html', {
        'quote': quote,
        'translation': translation,
        'title': 'Урок <strong>DJ02</strong>'
    })

def blog(request):
    return render(request, 'siteapp/blog.html', {
        'title': '<strong>Блог</strong>'})

def contacts(request):
    return render(request, 'siteapp/contacts.html', {
        'title': '<strong>Контакты</strong>'})


def form_view(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            if User.objects.filter(email=email).exists():
                messages.error(request, 'Этот email уже зарегистрирован.')
            else:
                form.save()
                messages.success(request, 'Пользователь успешно добавлен!')
                return redirect('form')  # Перенаправление на текущую страницу

    else:
        form = UserForm()

    users = User.objects.all()  # Получаем всех пользователей
    return render(request, 'siteapp/form.html', {'form': form, 'users': users})

def get_weather(request, city):
    API_KEY = 'fc4a628ded5e41efac0174832251904'  # Хранится только на сервере
    url = f'https://api.weatherapi.com/v1/current.json?key={API_KEY}&q={city}&lang=ru'

    try:
        response = requests.get(url)
        response.raise_for_status()
        return JsonResponse(response.json())
    except requests.exceptions.RequestException as e:
        return JsonResponse({'error': str(e)}, status=500)


MONTHS_RU = {
    1: 'января', 2: 'февраля', 3: 'марта', 4: 'апреля',
    5: 'мая', 6: 'июня', 7: 'июля', 8: 'августа',
    9: 'сентября', 10: 'октября', 11: 'ноября', 12: 'декабря'
}

def get_time(request):
    now = datetime.now()
    formatted_date = f"{now.day} {MONTHS_RU[now.month]} {now.year}"
    return JsonResponse({
        "time": now.strftime("%H:%M:%S"),
        "date": formatted_date
    })


def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            login(request, user)
            messages.success(request, f'Добро пожаловать, {user.username}!')
            return redirect('dashboard')
    else:
        form = RegisterForm()
    return render(request, 'siteapp/register.html', {'form': form, 'title': '<strong>Регистрация</strong>'})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            if not form.cleaned_data.get('remember_me'):
                request.session.set_expiry(0)
            return redirect('dashboard')
        else:
            # Ошибки уже будут в form.non_field_errors
            pass
    else:
        form = LoginForm(request)

    return render(request, 'siteapp/login.html', {
        'form': form,
        'title': '<strong>Вход в систему</strong>'
    })


@login_required
def dashboard_view(request):
    account = request.user
    user = User.objects.filter(email=account.email).first()
    return render(request, 'siteapp/account.html', {'account': account, 'user': user, 'title': '<strong>Личный кабинет</strong>'})

@login_required
def edit_account_view(request):
    account = request.user
    user = User.objects.filter(email=account.email).first()

    if request.method == 'POST':
        new_name = request.POST.get('name')
        new_email = request.POST.get('email')
        new_password = request.POST.get('password')
        city = request.POST.get('city')
        age = request.POST.get('age')
        hobby = request.POST.get('hobby')

        if Account.objects.filter(email=new_email).exclude(user_id=account.user_id).exists():
            messages.error(request, 'Этот email уже занят другим пользователем.')
            return redirect('edit_account')

        account.email = new_email
        if new_password:
            account.password = make_password(new_password)
        account.save()

        if user is None:
            user = User.objects.create(
                email=new_email,
                name=new_name,
                city=city,
                age=age,
                hobby=hobby
            )
        else:
            user.name = new_name
            user.email = new_email
            user.city = city
            user.age = age
            user.hobby = hobby
            user.save()

        messages.success(request, 'Данные успешно обновлены!')
        return redirect('dashboard')

    return render(request, 'siteapp/edit_account.html', {'account': account, 'user': user,'title': '<strong>Редактированние данных</strong>'})

@login_required
def logout_view(request):
    logout(request)
    messages.info(request, 'Вы вышли из системы.')
    return redirect('login')
