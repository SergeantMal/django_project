

# Create your models here.
from django.db import models

class User(models.Model):
    user_id = models.AutoField(primary_key=True)  # Устанавливаем user_id как первичный ключ
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    city = models.CharField(max_length=100)
    hobby = models.TextField()
    age = models.IntegerField()

    class Meta:
        db_table = 'users'  # Указываем нужное имя таблицы

    def __str__(self):
        return self.name
