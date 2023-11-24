# Generated by Django 4.2.7 on 2023-11-24 09:20

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Author',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_author', models.CharField(max_length=50, validators=[django.core.validators.MinLengthValidator(3)], verbose_name='Автор')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name_category', models.CharField(max_length=50, unique=True, verbose_name='Категория')),
            ],
        ),
        migrations.CreateModel(
            name='PostCategory',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('categories', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='categories', to='board_app.category')),
            ],
        ),
        migrations.CreateModel(
            name='Posts',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_post', models.CharField(max_length=100, validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Заголовок')),
                ('time_create', models.DateTimeField(auto_now_add=True, verbose_name='Дата создания')),
                ('time_update', models.DateTimeField(auto_now=True, verbose_name='Дата обновления')),
                ('text_post', models.TextField(validators=[django.core.validators.MinLengthValidator(5)], verbose_name='Текст обьявления')),
                ('file', models.ImageField(blank=True, upload_to='photos/%Y/%m/%d', verbose_name='Фотография')),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='author_posts', to='board_app.author')),
                ('categories', models.ManyToManyField(related_name='category_posts', through='board_app.PostCategory', to='board_app.category')),
            ],
            options={
                'ordering': ['-time_create'],
            },
        ),
        migrations.CreateModel(
            name='Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=50, verbose_name='Email')),
                ('status', models.CharField(choices=[('pending', 'Ожидает ответа'), ('accepted', 'Принят'), ('rejected', 'Отклонен')], default='pending', max_length=20)),
                ('posts', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe_posts', to='board_app.posts')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='subscribe_user', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='postcategory',
            name='posts',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posts', to='board_app.posts'),
        ),
    ]