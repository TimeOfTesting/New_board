from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinLengthValidator, MinValueValidator


class Category(models.Model):
    name_category = models.CharField(max_length=50, unique=True, null=False, verbose_name='Категория')

    def __str__(self):
        return self.name_category


class Author(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name_author = models.CharField(max_length=50, validators=[MinLengthValidator(3)], verbose_name='Автор')

    def __str__(self):
        return self.name_author


class Posts(models.Model):
    title_post = models.CharField(max_length=100, validators=[MinLengthValidator(5)], verbose_name='Заголовок')
    time_create = models.DateTimeField(auto_now_add=True,  verbose_name='Дата создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Дата обновления')
    text_post = models.TextField(validators=[MinLengthValidator(5)], verbose_name='Текст обьявления')
    file = models.ImageField(upload_to="photos/%Y/%m/%d", blank=True, verbose_name='Фотография')
    category = models.ManyToManyField(Category, related_name='category_posts', through='PostCategory')
    author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='author_posts')

    class Meta:
        ordering = ['-time_create']

    def __str__(self):
        return self.title_post

    def preview(self):
        return f'{self.text_post[:124]}...'

    def get_absolute_url(self):
        return f'/posts/{self.pk}'


class PostCategory(models.Model):
    categories = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='categories')
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='posts')

class Subscription(models.Model):
    pending = 'Ожидает ответа'
    accepted = 'Принят'
    rejected = 'Отклонен'

    response = [(pending, 'Ожидает ответа'), (accepted, 'Принят'), (rejected, 'Отклонен')]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='subscribe_user')
    posts = models.ForeignKey(Posts, on_delete=models.CASCADE, related_name='subscribe_posts')
    email = models.EmailField(max_length=50, verbose_name='Email')
    status = models.CharField(max_length=20, choices=response, default= pending)

    def __str__(self):
        return self.email

    def save(self, *args, **kwargs):
        self.post_author = self.posts.author
        super().save(*args, **kwargs)
