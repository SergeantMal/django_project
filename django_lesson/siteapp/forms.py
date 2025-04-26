from django import forms
from .models import User

class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['name', 'email', 'city', 'hobby', 'age']



from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from .models import Account


class RegisterForm(UserCreationForm):
    username = forms.CharField(label='Имя пользователя', error_messages={
        'unique': 'Пользователь с таким именем уже существует.',
        'required': 'Пожалуйста, введите имя пользователя.',
    })
    email = forms.EmailField(label='Email', error_messages={
        'unique': 'Пользователь с таким email уже существует.',
        'required': 'Пожалуйста, введите адрес электронной почты.',
        'invalid': 'Введите правильный email.',
    })
    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput, error_messages={
        'required': 'Пожалуйста, введите пароль.',
    })
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput, error_messages={
        'required': 'Пожалуйста, повторите пароль.',
    })


    class Meta:
        model = Account
        fields = ('username', 'email', 'password1', 'password2')




from django.contrib.auth.forms import AuthenticationForm
from django.core.exceptions import ValidationError

class LoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='Email',
        widget=forms.EmailInput(attrs={
            'autofocus': True,
            'class': 'form-control',
            'placeholder': 'Ваш email'
        }),
        error_messages={
            'required': 'Пожалуйста, введите email',
            'invalid': 'Введите правильный email адрес',
        }
    )
    password = forms.CharField(
        label='Пароль',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Ваш пароль'
        }),
        error_messages={
            'required': 'Пожалуйста, введите пароль',
        }
    )
    remember_me = forms.BooleanField(
        label='Запомнить меня',
        required=False,
        widget=forms.CheckboxInput(attrs={'class': 'form-check-input'})
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.error_messages.update({
            'invalid_login': "Неверный email или пароль. Оба поля могут быть чувствительны к регистру.",
        })


class BootstrapFormMixin:
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name, field in self.fields.items():
            widget = field.widget
            # Пропускаем CheckBox'ы, радиокнопки и пр.
            if not isinstance(widget, (forms.CheckboxInput, forms.RadioSelect)):
                widget.attrs['class'] = widget.attrs.get('class', '') + ' form-control'
            else:
                widget.attrs['class'] = widget.attrs.get('class', '') + ' form-check-input'
