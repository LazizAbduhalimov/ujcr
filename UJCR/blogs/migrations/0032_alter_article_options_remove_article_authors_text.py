# Generated by Django 4.0.2 on 2022-07-16 13:09

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0031_remove_authors_position_article_authors_text_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='article',
            options={'ordering': ['published_date', 'title'], 'verbose_name': 'Статью', 'verbose_name_plural': 'Статьи'},
        ),
        migrations.RemoveField(
            model_name='article',
            name='authors_text',
        ),
    ]