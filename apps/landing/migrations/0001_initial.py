# Generated by Django 3.2.4 on 2024-05-21 12:20

import core.files
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('city', '__first__'),
    ]

    operations = [
        migrations.CreateModel(
            name='Setup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('logotype', models.ImageField(blank=True, null=True, upload_to=core.files.upload_to, verbose_name='Логотип')),
                ('meta_title', models.TextField(blank=True, null=True, verbose_name='Заголовок сайта')),
                ('meta_keys', models.TextField(blank=True, null=True, verbose_name='Ключевые слова')),
                ('meta_desc', models.TextField(blank=True, null=True, verbose_name='Мета описание')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='e-mail для приёма заявок')),
                ('phone', models.CharField(blank=True, max_length=20, null=True, verbose_name='Контактный телефон')),
                ('video_find', models.CharField(blank=True, max_length=256, null=True, verbose_name='Видео: как найти наш офис')),
                ('video', models.TextField(blank=True, null=True, verbose_name='HTML-код видео: что получать наши клиенты')),
                ('top_js', models.TextField(blank=True, verbose_name='Скрипты в <HEAD>..</HEAD>')),
                ('bottom_js', models.TextField(blank=True, verbose_name='Скрипты перед закрывающим </BODY>')),
                ('robots_txt', models.TextField(blank=True, null=True, verbose_name='robots.txt')),
                ('city', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Настройки сайта',
                'verbose_name_plural': 'Настройки сайта',
                'ordering': ('id',),
            },
        ),
        migrations.CreateModel(
            name='BlockReview',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='ФИО')),
                ('image', models.ImageField(upload_to=core.files.upload_to, verbose_name='Фотография')),
                ('link', models.CharField(blank=True, max_length=256, null=True, verbose_name='ссылка')),
                ('description', models.TextField(verbose_name='Описание(компания, должность)')),
                ('text', models.TextField(verbose_name='Текст комментария')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Отзыв',
                'verbose_name_plural': 'Отзывы',
                'ordering': ('city',),
            },
        ),
        migrations.CreateModel(
            name='BlockExample',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, verbose_name='Название фотографии(адрес)')),
                ('image', models.ImageField(upload_to=core.files.upload_to, verbose_name='Фотография')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Прмеры размещений',
                'verbose_name_plural': 'Прмеры размещений',
                'ordering': ('city',),
            },
        ),
        migrations.CreateModel(
            name='BlockEffective',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to=core.files.upload_to, verbose_name='иконка')),
                ('text', models.TextField(verbose_name='Текст')),
                ('city', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='city.city', verbose_name='Город')),
            ],
            options={
                'verbose_name': 'Почему реклама настолько эффективна',
                'verbose_name_plural': 'Почему реклама настолько эффективна',
                'ordering': ('city',),
            },
        ),
    ]