# Generated by Django 4.0.2 on 2022-03-26 16:22

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0023_authors_slug'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='authors',
            options={'ordering': ['name'], 'verbose_name': 'Автора', 'verbose_name_plural': 'Авторы'},
        ),
    ]