from django.shortcuts import render, redirect
from django.http import JsonResponse
import requests
from datetime import datetime
from deep_translator import GoogleTranslator

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
        'title': 'Урок <strong>VD08</strong>'
    })

def blog(request):
    return render(request, 'siteapp/blog.html', {
        'title': '<strong>Блог</strong>'})

def contacts(request):
    return render(request, 'siteapp/contacts.html', {
        'title': '<strong>Контакты</strong>'})

from .forms import UserForm
from .models import User
from django.contrib import messages

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