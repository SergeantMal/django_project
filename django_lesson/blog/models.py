from django.db import models


class blog_post(models.Model):
    title = models.CharField('Название новости', max_length=50)
    short_description = models.CharField('Краткое описание новости', max_length=200)
    text = models.TextField('Новость')
    pub_date = models.DateTimeField('Дата публикации')
    author = models.CharField('Автор', max_length=50)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Новость'
        verbose_name_plural = 'Новости'
