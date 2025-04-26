from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

class AccountManager(BaseUserManager):
    def create_user(self, email, username, password=None, **extra_fields):
        if not email:
            raise ValueError('Email обязателен')
        if not username:
            raise ValueError('Имя пользователя обязательно')

        email = self.normalize_email(email)
        user = self.model(email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, username, password, **extra_fields)

class Account(AbstractBaseUser, PermissionsMixin):
    user_id = models.AutoField(primary_key=True)
    username = models.CharField('Имя пользователя', max_length=20, unique=True)
    email = models.EmailField('Электронная почта',max_length=120, unique=True)
    password = models.CharField('Пароль', max_length=255)

    last_login = models.DateTimeField(default=timezone.now)

    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = AccountManager()

    USERNAME_FIELD = 'email'          # 💥 Логинимся по email
    REQUIRED_FIELDS = ['username']    # 💥 Требуем username при регистрации

    groups = models.ManyToManyField(
        'auth.Group', related_name='custom_user_set', blank=True
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='custom_user_permissions', blank=True
    )

    class Meta:
        db_table = 'accounts'
        verbose_name = 'Аккаунт'
        verbose_name_plural = 'Аккаунты'

    def __str__(self):
        return f'User: {self.username}, email: {self.email}'

    def get_id(self):
        return str(self.user_id)

class User(models.Model):
    user_id = models.AutoField(primary_key=True)
    name = models.CharField('Имя', max_length=100)
    email = models.EmailField('Электронная почта', max_length=254, unique=True)
    city = models.CharField('Город', max_length=100)
    hobby = models.TextField('Хобби')
    age = models.IntegerField('Возраст')

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.name

from django.contrib.auth.backends import ModelBackend

class EmailBackend(ModelBackend):
    def authenticate(self, request, email=None, password=None, **kwargs):
        try:
            user = Account.objects.get(email=email)
            if user.check_password(password):
                return user
        except Account.DoesNotExist:
            return None