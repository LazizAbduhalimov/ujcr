# Generated by Django 4.0.2 on 2022-03-19 10:01

import ckeditor.fields
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=0)),
                ('title', models.CharField(default='', max_length=255, verbose_name='Должность')),
                ('title_ru', models.CharField(default='', max_length=255, null=True, verbose_name='Должность')),
                ('title_en', models.CharField(default='', max_length=255, null=True, verbose_name='Должность')),
            ],
            options={
                'verbose_name': 'Должность',
                'verbose_name_plural': 'Должности',
                'ordering': ['position'],
            },
        ),
        migrations.CreateModel(
            name='EditorialMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position', models.IntegerField(default=0)),
                ('full_name', models.CharField(default='', max_length=255, verbose_name='Ф.И.О.')),
                ('full_name_ru', models.CharField(default='', max_length=255, null=True, verbose_name='Ф.И.О.')),
                ('full_name_en', models.CharField(default='', max_length=255, null=True, verbose_name='Ф.И.О.')),
                ('location', models.CharField(default='', max_length=255, verbose_name='Место работы')),
                ('location_ru', models.CharField(default='', max_length=255, null=True, verbose_name='Место работы')),
                ('location_en', models.CharField(default='', max_length=255, null=True, verbose_name='Место работы')),
                ('about', ckeditor.fields.RichTextField(verbose_name='Об авторе')),
                ('about_ru', ckeditor.fields.RichTextField(null=True, verbose_name='Об авторе')),
                ('about_en', ckeditor.fields.RichTextField(null=True, verbose_name='Об авторе')),
                ('profile', ckeditor.fields.RichTextField(verbose_name='Профиль автора')),
                ('profile_ru', ckeditor.fields.RichTextField(null=True, verbose_name='Профиль автора')),
                ('profile_en', ckeditor.fields.RichTextField(null=True, verbose_name='Профиль автора')),
                ('address', models.CharField(default='', max_length=255, verbose_name='Адрес')),
                ('address_ru', models.CharField(default='', max_length=255, null=True, verbose_name='Адрес')),
                ('address_en', models.CharField(default='', max_length=255, null=True, verbose_name='Адрес')),
                ('phone_number', models.CharField(default='', max_length=255, verbose_name='Номер телефона')),
                ('e_mail', models.EmailField(max_length=255, verbose_name='E-mail')),
                ('e_mail_ru', models.EmailField(max_length=255, null=True, verbose_name='E-mail')),
                ('e_mail_en', models.EmailField(max_length=255, null=True, verbose_name='E-mail')),
                ('post', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.post', verbose_name='Занимаемая должность')),
                ('post_en', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.post', verbose_name='Занимаемая должность')),
                ('post_ru', models.ForeignKey(null=True, on_delete=django.db.models.deletion.DO_NOTHING, to='main_app.post', verbose_name='Занимаемая должность')),
            ],
            options={
                'verbose_name': 'Участника редакции',
                'verbose_name_plural': 'Редакция',
                'ordering': ['position'],
            },
        ),
    ]
