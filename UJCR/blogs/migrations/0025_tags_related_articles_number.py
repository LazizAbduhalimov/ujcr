# Generated by Django 4.0.2 on 2022-03-30 16:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0024_alter_authors_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='tags',
            name='related_articles_number',
            field=models.IntegerField(default=0, verbose_name='Количество связанных статей'),
        ),
    ]
