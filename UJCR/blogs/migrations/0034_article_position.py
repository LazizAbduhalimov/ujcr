# Generated by Django 4.0.2 on 2022-07-16 13:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0033_remove_article_position'),
    ]

    operations = [
        migrations.AddField(
            model_name='article',
            name='position',
            field=models.IntegerField(default=0),
        ),
    ]
