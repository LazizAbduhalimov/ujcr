# Generated by Django 4.0.2 on 2022-03-19 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0002_post_editorialmember'),
    ]

    operations = [
        migrations.AddField(
            model_name='editorialmember',
            name='slug',
            field=models.SlugField(blank=True, max_length=200, unique=True, verbose_name='Slug страницы'),
        ),
    ]