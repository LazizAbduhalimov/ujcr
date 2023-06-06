# Generated by Django 4.0.2 on 2023-04-16 11:12

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ReviewersProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, default='', max_length=255, verbose_name='Имя, Фамилия')),
                ('full_name_ru', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Имя, Фамилия')),
                ('full_name_en', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Имя, Фамилия')),
                ('slug', models.SlugField(blank=True, max_length=200, verbose_name='Slug статьи')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='reviewer_user', to=settings.AUTH_USER_MODEL, verbose_name='Зарегестрированный пользователь')),
            ],
            options={
                'verbose_name': 'Рецензента',
                'verbose_name_plural': 'Рецензенты',
            },
        ),
        migrations.CreateModel(
            name='AuthorsProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('full_name', models.CharField(blank=True, default='', max_length=255, verbose_name='Имя, Фамилия')),
                ('full_name_ru', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Имя, Фамилия')),
                ('full_name_en', models.CharField(blank=True, default='', max_length=255, null=True, verbose_name='Имя, Фамилия')),
                ('slug', models.SlugField(blank=True, max_length=200, verbose_name='Slug статьи')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, related_name='author_user', to=settings.AUTH_USER_MODEL, verbose_name='Зарегестрированный пользователь')),
            ],
            options={
                'verbose_name': 'Автора',
                'verbose_name_plural': 'Авторы',
            },
        ),
    ]
