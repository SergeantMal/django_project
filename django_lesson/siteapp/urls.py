from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog', views.blog, name='blog'),
    path('form', views.form_view, name='form'),
    path('contacts', views.contacts, name='contacts'),
    path('api/weather/<str:city>/', views.get_weather, name='get_weather'),
    path('time/', views.get_time, name='get_time')
]
from django.http import HttpResponse