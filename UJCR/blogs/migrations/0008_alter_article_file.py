# Generated by Django 4.0.2 on 2022-03-08 11:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blogs', '0007_remove_volume_file_article_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='article',
            name='file',
            field=models.FileField(null=True, upload_to='files/Article/', verbose_name='Файл (PDF)'),
        ),
    ]