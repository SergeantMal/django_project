from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('form/', views.form_view, name='form'),
    path('contacts/', views.contacts, name='contacts'),
    path('api/weather/<str:city>/', views.get_weather, name='get_weather'),
    path('time/', views.get_time, name='get_time'),
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('account/', views.dashboard_view, name='dashboard'),
    path('account/edit/', views.edit_account_view, name='edit_account'),
    path('logout/', views.logout_view, name='logout')
]
from django.http import HttpResponse