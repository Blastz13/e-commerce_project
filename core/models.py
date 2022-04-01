from django.db import models
from django.utils import timezone
from django.shortcuts import reverse
from ckeditor_uploader.fields import RichTextUploadingField

from .utils import path_upload


class Feed(models.Model):
    title = models.CharField(max_length=128, blank=True, db_index=True, default='', verbose_name='Заголовок')
    sup_title = models.CharField(max_length=128, blank=True, default='', verbose_name='Подзаголовок')
    description = models.CharField(max_length=512, blank=True, default='', verbose_name='Описание')
    body = RichTextUploadingField()
    image = models.ImageField(upload_to=path_upload('Feed'), default='default_img/news.jpeg', blank=True, null=True,
                              verbose_name='Изображение')
    slug = models.SlugField(max_length=128, unique=True, db_index=True, verbose_name='Ссылка на новость')
    category = models.ForeignKey('CategoryFeed', on_delete=models.CASCADE, verbose_name='Категория')
    text_button = models.CharField(max_length=64, blank=True, default='', verbose_name='Надпись кнопки')
    url_button = models.SlugField(max_length=512, blank=True, default='', verbose_name='Ссылка кнопки')
    is_slider = models.BooleanField(default=False, verbose_name='Слайдер')
    is_blog = models.BooleanField(default=False, verbose_name='Блог')
    is_publish = models.BooleanField(default=False, verbose_name='Опубликовать')
    date_publicate = models.DateTimeField(auto_now_add=True, verbose_name='Дата публикации')
    date_published_from = models.DateTimeField(default=timezone.now, blank=True, null=True,
                                               verbose_name="Опубликовать c")
    date_published_to = models.DateTimeField(default=timezone.now() + timezone.timedelta(days=7), blank=True, null=True,
                                             verbose_name="Опубликовать до")
    tag = models.ManyToManyField('Tag', blank=True, related_name='feeds', verbose_name='Тэг')

    def get_absolute_url(self):
        return reverse('FeedDetail', kwargs={
            'category': self.category.slug,
            'slug': self.slug
        })

    def get_comments(self):
        return self.comments.filter(parent__isnull=True)

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['-date_publicate']
        verbose_name = "Новость"
        verbose_name_plural = "Новости"


class CategoryFeed(models.Model):
    title = models.CharField(max_length=64, unique=True, verbose_name='Название категории')
    slug = models.SlugField(max_length=128, unique=True, db_index=True, verbose_name='Ссылка на категорию')

    def get_absolute_url(self):
        return reverse('FeedListCategory', kwargs={'category': self.slug})

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['title']
        verbose_name = "Категория"
        verbose_name_plural = "Категории"


class Tag(models.Model):
    title = models.CharField(max_length=50, verbose_name="Название")
    slug = models.SlugField(max_length=50, unique=True, verbose_name="Ссылка")

    def get_absolute_url(self):
        return reverse('FeedListTag', kwargs={"slug": self.slug})

    def __str__(self):
        return str(self.title)

    class Meta:
        verbose_name = "Тэг"
        verbose_name_plural = "Тэги"


class Comment(models.Model):
    email = models.EmailField(verbose_name='Почта')
    name = models.CharField(max_length=100, verbose_name="Имя")
    text = models.TextField(max_length=5000, verbose_name="Сообщение")
    date_publicate = models.DateTimeField(auto_now_add=True, verbose_name="Дата добавления")
    parent = models.ForeignKey("self", verbose_name="Родитель", on_delete=models.SET_NULL, blank=True, null=True)
    feed = models.ForeignKey(Feed, related_name="comments", on_delete=models.CASCADE, verbose_name="Новость")

    def __str__(self):
        return f"{self.name} - {self.feed}"

    class Meta:
        ordering = ["-date_publicate"]
        verbose_name = "Комментарий"
        verbose_name_plural = "Комментарии"


class OurBrand(models.Model):
    title = models.CharField(max_length=128, db_index=True, blank=True, verbose_name='Название бренда')
    image = models.ImageField(upload_to=path_upload('OurBrands'), verbose_name='Логотип')
    order = models.IntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return "{}".format(self.title)

    class Meta:
        ordering = ['order']
        verbose_name = "Наши бренды"
        verbose_name_plural = "Наши бренды"


class ContactForm(models.Model):
    name = models.CharField(max_length=64, verbose_name='Имя')
    email = models.EmailField(verbose_name='Почта')
    subject = models.CharField(max_length=64, verbose_name='Тема')
    message = models.TextField(max_length=1000, verbose_name='Сообщение')
    date_send = models.DateTimeField(auto_now_add=True, verbose_name='Дата отправки')

    def __str__(self):
        return "{0} - {1}, {2}".format(self.email, self.subject, self.date_send)

    class Meta:
        ordering = ['-date_send']
        verbose_name = "Сообщения контактной формы"
        verbose_name_plural = "Сообщения контактной формы"


class ContactAddress(models.Model):
    title = models.CharField(max_length=64, blank=True, verbose_name='Заголовок')
    address = models.CharField(max_length=128, verbose_name='Адрес')
    phone = models.CharField(max_length=12, blank=True, verbose_name='Телефон')
    email = models.EmailField(blank=True, verbose_name='Почта')
    order = models.PositiveIntegerField(default=0, verbose_name='Порядок')

    def __str__(self):
        return "{0} - {1}, {2}".format(self.address, self.phone, self.email)

    class Meta:
        ordering = ['order']
        verbose_name = "Контактный адрес"
        verbose_name_plural = "Контактные адреса"
